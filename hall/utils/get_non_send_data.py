from datetime import datetime, timedelta

from hall.models import Device
from device.models import HeadData


def get_count_non_send(query_set):
    timeline = datetime.now() - timedelta(minutes=5)
    device_head_data = list(
        HeadData.objects.filter(receive_at__gt=timeline).distinct().values_list("device_id", flat=True))
    return len(query_set.filter(is_connected=True, id__in=device_head_data))
