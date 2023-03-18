from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid
import os


@csrf_exempt
def upload_media(request):

    media = request.FILES.get('media')

    extension = os.path.splitext(str(media))[1]
    unique_filename = uuid.uuid4().hex
    # print(f"extension :: {extension}")
    # print(f"unique_filename :: {unique_filename}")
    
    media_type = "others"
    if extension.lower() in ['.jpg', '.png', '.jpeg']:
        media_type = "image"
    
    else:
        return JsonResponse({"url": None})
    
    dest_folder = f"parking_places/{media_type}"
    # print("dest_folder :: ", dest_folder)
    # Path(dest_folder).mkdir(parents=True, exist_ok=True) # keep this commented

    dest = f"{dest_folder}/{unique_filename}{extension}"
    # print(dest)

    fs = FileSystemStorage()
    filename = fs.save(dest, media)
    media_url = fs.url(filename)
    # print(media_url)

    # url = f"https://dskolwankar1.pagekite.me{media_url}"
    url = f"http://127.0.0.1:8000{media_url}"
    
    print(url)

    return JsonResponse({"url": url})


