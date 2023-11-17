import datetime
import json
from datetime import datetime, timedelta

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count

from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import View, Event


class CtrAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            start_date = datetime.strptime(data.get('startDate'), '%d.%m.%Y')
            end_date = datetime.strptime(data.get('endDate'), '%d.%m.%Y')

            result_data = {}

            current_date = start_date
            while current_date <= end_date:
                current_date_str = current_date.strftime('%Y-%m-%d')

                views = View.objects.filter(reg_time__date=current_date_str).only('uid')
                v_list = list(views.values_list('uid', flat=True))
                impression_count = views.count()

                if impression_count == 0:
                    click_count = 0
                    ctr = 0
                else:
                    events = Event.objects.filter(tag='fclick', uid__in=v_list)
                    click_count = events.count()
                    ctr = round(100 * (click_count / impression_count), 2)

                result_data[current_date_str] = ctr
                current_date += timedelta(days=1)

            return JsonResponse(result_data)

        except json.JSONDecodeError as e:
            # Обработка ошибок JSON
            return JsonResponse({'error': 'Incorrect data'}, status=400)

        except Exception as e:
            # Обработка других исключений
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        return render(request, 'metrics/ctr.html')


class EvpmAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            start_date = datetime.strptime(data.get('startDate'), '%d.%m.%Y')
            end_date = datetime.strptime(data.get('endDate'), '%d.%m.%Y')
            tag = data.get('tag')

            result_data = {}

            # Обработка данных для каждой даты в диапазоне
            current_date = start_date
            while current_date <= end_date:
                current_date_str = current_date.strftime('%Y-%m-%d')

                # Фильтрация для текущей даты
                views = View.objects.filter(reg_time__date=current_date_str).only('uid')
                v_list = list(views.values_list('uid', flat=True))
                impression_count = views.count()

                if impression_count == 0:
                    event_count = 0
                    evpm = 0
                else:
                    events = Event.objects.filter(tag__contains=tag, uid__in=v_list)
                    event_count = events.count()
                    evpm = round(1000 * (event_count / impression_count), 2)

                result_data[current_date_str] = evpm
                current_date += timedelta(days=1)

            return JsonResponse(result_data)

        except json.JSONDecodeError as e:
            # Обработка ошибок JSON
            return JsonResponse({'error': 'Incorrect data'}, status=400)

        except Exception as e:
            # Обработка других исключений
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        try:
            tags_list = list(Event.objects.all().values_list('tag', flat=True))

            tags = [tag[1:] if tag.startswith('v') else tag for tag in tags_list]
            tags = list(dict.fromkeys(tags))

            return render(request, 'metrics/evpm.html', {'events': tags})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AggregationAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            start_date = datetime.strptime(data.get('startDate'), '%d.%m.%Y')
            end_date = datetime.strptime(data.get('endDate'), '%d.%m.%Y')
            aggregation_type = data.get('aggregationType')
            tag = data.get('tag')
            result_data = []

            views = View.objects.filter(reg_time__range=(start_date, end_date))
            aggregation_data = views.values(aggregation_type).annotate(
                impression_count=Count('id'),
                list_uid=ArrayAgg('uid'),
            ).values('impression_count', 'list_uid', aggregation_type)

            for data in aggregation_data:
                click_count = Event.objects.filter(tag='fclick', uid__in=data['list_uid']).count()
                event_count = Event.objects.filter(tag=tag, uid__in=data['list_uid']).count()

                if data['impression_count'] == 0:
                    ctr = 0
                    evpm = 0
                else:
                    ctr = round(100 * (click_count / data['impression_count']), 2)
                    evpm = round(1000 * (event_count / data['impression_count']), 2)

                result_data.append({
                    aggregation_type: data[aggregation_type],
                    'impression_count': data['impression_count'],
                    'ctr': ctr,
                    'evpm': evpm
                })

            return JsonResponse(result_data, safe=False)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Incorrect data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        tags_list = list(Event.objects.all().values_list('tag', flat=True))
        tags = []
        for tag in tags_list:
            if tag.startswith('v'):
                tag = tag[1:]
            tags.append(tag)
        tags = list(dict.fromkeys(tags))
        return render(request, 'metrics/aggregation.html', {'events': tags})