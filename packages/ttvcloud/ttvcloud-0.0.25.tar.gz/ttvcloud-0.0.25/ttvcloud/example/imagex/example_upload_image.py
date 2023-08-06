# coding:utf-8
from __future__ import print_function
import os
from ttvcloud.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()
    imagex_service.set_host("staging-openapi-boe.byted.org")

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imagex_service.set_ak('AKLTMjY5N2YxMTlhNDY1NDhlMTg3NGJiNDQxZjM5NmY4NmE')
    imagex_service.set_sk('QXeJoMRRGc9RgLK+sBrJ2Mdumm3O72kpRFoTqm/GybYPCrjiduJnrxHu7Z+Eyobh')

    service_id = '241hsrmp5z'
    file_paths = ['/Users/yefu/Downloads/test.png', '/Users/yefu/Downloads/10001.jpg']

    resp = imagex_service.upload_image(service_id, file_paths)
    print(resp)

    img_datas = []
    for p in file_paths:
        if not os.path.isfile(p):
            raise Exception("no such file on file path %s" % p)
        in_file = open(p, "rb")
        img_datas.append(in_file.read())
        in_file.close()

    resp = imagex_service.upload_image_data(service_id, img_datas)
    print(resp)
