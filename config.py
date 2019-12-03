# 请修改为对应的oss可用区
# https://www.alibabacloud.com/help/zh/doc-detail/31837.htm
# 如果部署在阿里云，可以使用内网地址。
REGION = 'cn-shanghai'
BUCKET_API_ENDPOINT = f'https://oss-{REGION}.aliyuncs.com'

# 请修改为您的oss bucket名
BUCKET_NAME = ''
BUCKET_HOST = f'https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com'

BUCKET_API_KEY = ''
BUCKET_API_SECRET = ''

# 字体名
FAMILY_NAME = 'MyAwesomeFont'
STYLE_NAME = 'Regular'

# 一些meta信息，请修改
NAME_STRING = {
    'familyName': FAMILY_NAME,
    'styleName': STYLE_NAME,
    'psName': FAMILY_NAME + '-' + STYLE_NAME,
    'copyright': 'Created by solarhell',
    'version': 'Version 1.0',
    'vendorURL': 'https://solarhell.com/',
}
