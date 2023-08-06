from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from main.models.arx_attatch import Arx_attatch
from main.models.arx_docizv import Arx_docizv
from main.models.arx_upload_file import DSResponse_Arx_UploadFile


class RemoveFile(DSResponse_Arx_UploadFile):
    def __init__(self, request):
        request = DSRequest(request=request)
        table_name = request.json.get('table_name')
        old_id = request.json.get('old_id')

        if table_name == 'attatch' and old_id:
            Arx_attatch.objects.filter(id=old_id).delete()

        if table_name == 'doc_izv' and old_id:
            Arx_docizv.objects.filter(id=old_id).delete()

        self.response = dict(status=RPCResponseConstant.statusSuccess)


@JsonWSResponseWithException(printing=False)
def Common_RemoveFile(request):
    return JsonResponse(RemoveFile(request).response)
