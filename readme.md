```cmd
docker build -t paddle_ocr_server:1.0.1  .
```

```cmd
docker run --name paddle_ocr_server  -p 2020:2020 paddle_ocr_server:1.0.1
```
##图片下载链接请求地址
```cmd
127.0.0.1:2020/api/v1/ocr
```
##图片base64编码下载链接请求地址
```
127.0.0.1:2020/api/base64/ocr
```