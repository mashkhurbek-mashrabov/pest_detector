import datetime
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from detector.detect import pest_detector
from farmer.models import FarmerArea, Report


def report_receiver(request):
    if request.method == 'GET' and request.FILES.get('image'):
        data = request.POST
        image_file = request.FILES['image']
        image_data = image_file.read()

        saved_image_path, detection_results = pest_detector(image_data)

        area_id = data.get('area_id')
        sensor_id = data.get('sensor_id')

        area = FarmerArea.objects.get(id=area_id)

        # Convert the image path to an InMemoryUploadedFile
        with open(saved_image_path, 'rb') as image_file:
            django_image = InMemoryUploadedFile(
                file=image_file,
                field_name=None,
                name=os.path.basename(saved_image_path),
                content_type='image/jpeg',
                size=os.path.getsize(saved_image_path),
                charset=None
            )

            # Create and save the Report instance
            report = Report(area=area,
                            sensor_id=sensor_id,
                            image=django_image,
                            data=detection_results,
                            created_at=datetime.datetime.now())
            report.save()

        return JsonResponse(status=200)
    else:
        return JsonResponse(status=400)
