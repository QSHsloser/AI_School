from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
import logging

# 配置日志记录
logger = logging.getLogger(__name__)

from ai_edu.models import Book, Student, Teacher, Classroom


# Create your views here.
def add_book(request):
    response = {}
    try:
        book = Book(name=request.GET.get('name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    
    return JsonResponse(response)








@csrf_exempt
def get_current_user(request):
    response = {}
    try:
        if request.user.is_authenticated:
            response['msg'] = '已登录'
            response['error_num'] = 0
            response['username'] = request.user.username
            response['is_authenticated'] = True
        else:
            response['msg'] = '未登录'
            response['error_num'] = 0
            response['is_authenticated'] = False
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    
    return JsonResponse(response)


@csrf_exempt
def login_user(request):
    response = {}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user_type = data.get('user_type', 'student')
            
            if not username or not password:
                response['msg'] = '用户名和密码不能为空'
                response['error_num'] = 1
                return JsonResponse(response)
            
            if user_type == 'student':
                try:
                    student = Student.objects.get(username=username)
                    if check_password(password, student.password):
                        response['msg'] = '学生登录成功'
                        response['error_num'] = 0
                        response['username'] = student.username
                        response['user_type'] = 'student'
                    else:
                        response['msg'] = '学生用户名或密码错误'
                        response['error_num'] = 1
                except Student.DoesNotExist:
                    response['msg'] = '学生用户名或密码错误'
                    response['error_num'] = 1
            elif user_type == 'teacher':
                try:
                    teacher = Teacher.objects.get(username=username)
                    if check_password(password, teacher.password):
                        response['msg'] = '教师登录成功'
                        response['error_num'] = 0
                        response['username'] = teacher.username
                        response['user_type'] = 'teacher'
                    else:
                        response['msg'] = '教师用户名或密码错误'
                        response['error_num'] = 1
                except Teacher.DoesNotExist:
                    response['msg'] = '教师用户名或密码错误'
                    response['error_num'] = 1
            else:
                response['msg'] = '用户类型错误'
                response['error_num'] = 1
        else:
            response['msg'] = '请使用POST请求'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    
    return JsonResponse(response)



def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def classrooms(request):
    response = {}
    try:
        classes = Classroom.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", classes))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
def register(request):
    response = {}
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user_type = data.get('user_type', 'student')
            
            if not username or not password:
                response['msg'] = '用户名和密码不能为空'
                response['error_num'] = 1
                return JsonResponse(response)
            
            hashed_password = make_password(password)
            
            if user_type == 'student':
                if Student.objects.filter(username=username).exists():
                    response['msg'] = '学生用户名已存在'
                    response['error_num'] = 1
                    return JsonResponse(response)
                student = Student(
                    username=username,
                    password=hashed_password,
                    teacher_id=0  # 默认教师ID
                )
                student.save()
                response['msg'] = '学生注册成功'
                response['error_num'] = 0
                response['username'] = username
                response['user_type'] = 'student'
            elif user_type == 'teacher':
                if Teacher.objects.filter(username=username).exists():
                    response['msg'] = '教师用户名已存在'
                    response['error_num'] = 1
                    return JsonResponse(response)
                teacher_id = data.get('id', Teacher.objects.count() + 1)
                teacher = Teacher(
                    id=teacher_id,
                    username=username,
                    password=hashed_password
                )
                teacher.save()
                response['msg'] = '教师注册成功'
                response['error_num'] = 0
                response['username'] = username
                response['user_type'] = 'teacher'
            else:
                response['msg'] = '用户类型错误'
                response['error_num'] = 1
                return JsonResponse(response)
        else:
            response['msg'] = '请使用POST请求'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    
    return JsonResponse(response)


@csrf_exempt
def dify_chat(request):
    """Dify流式对话API接口，支持文件上传"""
    try:
        logger.info(f"Received request to dify_chat: method={request.method}, headers={dict(request.headers)}")
        
        if request.method != 'POST':
            logger.warning(f"Invalid method {request.method} to dify_chat")
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
        # 检查Content-Type
        content_type = request.headers.get('Content-Type')
        logger.info(f"Request Content-Type: {content_type}")
        
        # 解析请求数据
        user_message = None
        user_type = None
        username = None
        files = None
        
        # 根据不同的Content-Type处理请求
        if content_type and content_type.startswith('multipart/form-data'):
            # 处理文件上传请求
            logger.info("Processing multipart/form-data request")
            user_message = request.POST.get('message')
            user_type = request.POST.get('user_type')
            username = request.POST.get('username')
            files = request.FILES
            logger.info(f"Files: {files}")
        elif content_type == 'application/json':
            # 处理JSON请求
            logger.info("Processing application/json request")
            if not request.body:
                logger.warning("Empty request body")
                return JsonResponse({'error': 'Request body cannot be empty'}, status=400)
            
            try:
                data = json.loads(request.body)
                logger.info(f"Parsed request data: {data}")
                user_message = data.get('message')
                user_type = data.get('user_type')
                username = data.get('username')
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}, request body: {request.body}")
                return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        else:
            logger.warning(f"Invalid Content-Type {content_type}")
            return JsonResponse({'error': 'Content-Type must be application/json or multipart/form-data'}, status=400)
        
        # 验证参数
        logger.info(f"User message: {user_message}, user type: {user_type}, username: {username}")
        
        if not user_message:
            logger.warning("Empty user message")
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        if not username:
            logger.warning("Empty username")
            return JsonResponse({'error': 'Username cannot be empty'}, status=400)
        
        # 获取Dify API配置
        DIFY_API_URL = getattr(settings, 'DIFY_API_URL', 'https://api.dify.ai/v1/chat-messages')
        DIFY_API_KEY = getattr(settings, 'DIFY_API_KEY', {})
        
        api_key = DIFY_API_KEY.get(user_type)
        if not api_key:
            return JsonResponse({'error': 'API key not found for this user type'}, status=500)
        
        # 构建请求数据
        dify_payload = {
            'inputs': {},
            'query': user_message,
            'response_mode': 'streaming',
            'user': username
        }
        
        headers = {
            'Authorization': f'Bearer {api_key}',
        }
        
        # 处理流式响应
        def stream_response():
            # 处理请求 - 始终使用JSON格式
            # 如果有文件，先上传获取文件ID
            file_ids = []
            if files:
                # 构建文件上传请求的URL
                file_upload_url = getattr(settings, 'DIFY_FILE_UPLOAD_URL', 'https://api.dify.ai/v1/files/upload')
                
                # 只上传第一个文件，因为Dify API只允许单次上传一个文件
                file_key = next(iter(files))
                file = files[file_key]
                # 准备文件上传数据 - Dify API要求文件放在files参数，user放在data参数
                upload_files = {
                    'file': (file.name, file.file, file.content_type)
                }
                upload_data = {
                    'user': username  # user参数需要单独放在data中，与files分开
                }
                
                try:
                    # 上传文件
                    logger.info(f"Uploading file to {file_upload_url} with headers: {headers}")
                    upload_response = requests.post(
                        file_upload_url, 
                        files=upload_files, 
                        data=upload_data,
                        headers=headers
                    )
                    logger.info(f"File upload response status: {upload_response.status_code}, response: {upload_response.text}")
                    
                    # 检查文件上传是否成功（200或201都视为成功）
                    if upload_response.status_code < 200 or upload_response.status_code >= 300:
                        yield json.dumps({'error': f'File upload failed: {upload_response.text}'}).encode('utf-8') + b'\n'
                        return
                    
                    # 解析上传结果
                    try:
                        upload_result = upload_response.json()
                        logger.info(f"File upload result parsed: {upload_result}")
                        file_id = upload_result.get('id')
                        logger.info(f"Extracted file_id: {file_id}")
                        if file_id:
                            file_ids.append(file_id)
                            logger.info(f"Added file_id to list: {file_ids}")
                        else:
                            logger.warning(f"No file_id found in upload response: {upload_result}")
                            yield json.dumps({'error': f'No file_id found in upload response'}).encode('utf-8') + b'\n'
                            return
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse file upload response as JSON: {str(e)}, response text: {upload_response.text}")
                        yield json.dumps({'error': f'Failed to parse file upload response: {str(e)}'}).encode('utf-8') + b'\n'
                        return
                except Exception as e:
                    yield json.dumps({'error': f'File upload exception: {str(e)}'}).encode('utf-8') + b'\n'
                    return
            
            # 准备聊天请求数据
            chat_data = dify_payload.copy()
            
            # 如果有文件ID，添加到请求数据中 - 使用Dify API要求的格式
            if file_ids:
                chat_data['files'] = [{'type': 'document', 'transfer_method': 'local_file', 'upload_file_id': file_id} for file_id in file_ids]
            
            # 发送JSON格式的请求
            with requests.post(DIFY_API_URL, json=chat_data, headers=headers, stream=True) as r:
                if r.status_code != 200:
                    yield json.dumps({'error': f'Dify API error: {r.text}'}).encode('utf-8') + b'\n'
                    return
                
                buffer = b''
                # 使用iter_content获取字节流，确保decode_unicode=False
                for chunk in r.iter_content(chunk_size=None, decode_unicode=False):
                    if chunk:
                        buffer += chunk
                        # 按行分割，处理完整的行
                        while b'\n' in buffer:
                            line, buffer = buffer.split(b'\n', 1)
                            if line.startswith(b'data: '):
                                json_str = line[6:]
                                if json_str.strip() == b'[DONE]':
                                    yield json.dumps({'done': True}).encode('utf-8') + b'\n'
                                else:
                                    try:
                                        # 尝试解码为UTF-8并解析为JSON
                                        # 使用errors='replace'处理特殊字符
                                        json_data = json.loads(json_str.decode('utf-8', errors='replace'))
                                        yield json.dumps(json_data).encode('utf-8') + b'\n'
                                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                                        # 记录错误但继续处理
                                        logger.warning(f"Failed to parse JSON: {e}, raw data: {json_str[:100]}...")
                                        continue
                            else:
                                # 不是以'data: '开头的行，可能是错误信息或其他内容
                                try:
                                    # 尝试解码为UTF-8并记录
                                    line_content = line.decode('utf-8', errors='replace')
                                    logger.info(f"Received non-data line: {line_content}")
                                except UnicodeDecodeError as e:
                                    logger.warning(f"Failed to decode line: {e}, raw data: {line[:100]}...")
                                    continue
                # 处理剩余的缓冲内容
                if buffer.startswith(b'data: '):
                    json_str = buffer[6:]
                    if json_str.strip() == b'[DONE]':
                        yield json.dumps({'done': True}).encode('utf-8') + b'\n'
                    else:
                        try:
                            # 尝试解码为UTF-8并解析为JSON
                            json_data = json.loads(json_str.decode('utf-8', errors='replace'))
                            yield json.dumps(json_data).encode('utf-8') + b'\n'
                        except (json.JSONDecodeError, UnicodeDecodeError) as e:
                            # 记录错误但继续处理
                            logger.warning(f"Failed to parse JSON: {e}, raw data: {json_str[:100]}...")
                            pass
        
        return StreamingHttpResponse(stream_response(), content_type='application/json')
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        logger.error(f"Error in dify_chat: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def dify_file_preview(request):
    """Dify文件预览API接口，支持预览和下载"""
    try:
        logger.info(f"Received request to dify_file_preview: method={request.method}, headers={dict(request.headers)}")
        logger.info(f"Request GET params: {request.GET}")
        logger.info(f"Request full path: {request.get_full_path()}")
        
        if request.method != 'GET':
            logger.warning(f"Invalid method {request.method} to dify_file_preview")
            return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
        
        # 获取文件ID、用户类型和下载参数
        file_id = request.GET.get('file_id')
        user_type = request.GET.get('user_type')
        as_attachment = request.GET.get('as_attachment', 'false').lower() == 'true'
        
        logger.info(f"File ID: {file_id}, user type: {user_type}, as_attachment: {as_attachment}")
        
        if not file_id:
            logger.warning("Empty file ID")
            return JsonResponse({'error': 'File ID cannot be empty'}, status=400)
        
        # 获取Dify API配置
        DIFY_FILE_API_URL = getattr(settings, 'DIFY_FILE_API_URL', 'https://api.dify.ai/v1/files')
        DIFY_API_KEY = getattr(settings, 'DIFY_API_KEY', {})
        
        logger.info(f"DIFY_FILE_API_URL: {DIFY_FILE_API_URL}")
        logger.info(f"DIFY_API_KEY keys: {list(DIFY_API_KEY.keys())}")
        
        api_key = DIFY_API_KEY.get(user_type)
        if not api_key:
            logger.error(f"API key not found for user type: {user_type}")
            return JsonResponse({'error': 'API key not found for this user type'}, status=500)
        
        # 构建请求头
        headers = {
            'Authorization': f'Bearer {api_key}',
        }
        logger.info(f"Request headers: {headers}")
        
        # 构建请求URL - 根据Dify文档，使用/preview端点支持预览和下载
        file_url = f"{DIFY_FILE_API_URL}/{file_id}/preview"
        logger.info(f"Constructed file URL: {file_url}")
        
        # 构建查询参数
        params = {
            'as_attachment': str(as_attachment).lower()
        }
        logger.info(f"Request params: {params}")
        
        # 处理流式响应
        def stream_file():
            logger.info(f"Making request to Dify API: {file_url}")
            with requests.get(file_url, headers=headers, params=params, stream=True) as r:
                logger.info(f"Dify API response status: {r.status_code}")
                logger.info(f"Dify API response headers: {dict(r.headers)}")
                
                if r.status_code != 200:
                    logger.error(f"Dify API error: status={r.status_code}, response={r.text}")
                    yield json.dumps({'error': f'Dify API error: {r.text}'}).encode('utf-8') + b'\n'
                    return
                
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
        
        # 获取文件信息和内容类型
        try:
            info_response = requests.get(f"{DIFY_FILE_API_URL}/{file_id}", headers=headers)
            if info_response.status_code == 200:
                file_info = info_response.json()
                content_type = file_info.get('mime_type', 'application/octet-stream')
                filename = file_info.get('name', file_id)
            else:
                content_type = 'application/octet-stream'
                filename = file_id
        except Exception as e:
            logger.warning(f"Failed to get file info: {str(e)}")
            content_type = 'application/octet-stream'
            filename = file_id
        
        # 创建响应
        response = StreamingHttpResponse(stream_file())
        
        # 设置响应头
        response['Content-Type'] = content_type
        if as_attachment:
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{filename}"'
        
        return response
    
    except Exception as e:
        logger.error(f"Error in dify_file_preview: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def dify_stop_response(request):
    """Dify停止响应API接口"""
    try:
        logger.info(f"Received request to dify_stop_response: method={request.method}, headers={dict(request.headers)}")
        
        if request.method != 'POST':
            logger.warning(f"Invalid method {request.method} to dify_stop_response")
            return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        
        # 解析请求数据
        try:
            data = json.loads(request.body)
            logger.info(f"Parsed request data: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}, request body: {request.body}")
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        
        # 获取会话ID和用户类型
        conversation_id = data.get('conversation_id')
        user_type = data.get('user_type')
        
        logger.info(f"Conversation ID: {conversation_id}, user type: {user_type}")
        
        if not conversation_id:
            logger.warning("Empty conversation ID")
            return JsonResponse({'error': 'Conversation ID cannot be empty'}, status=400)
        
        # 获取Dify API配置
        DIFY_STOP_API_URL = getattr(settings, 'DIFY_STOP_API_URL', 'https://api.dify.ai/v1/conversations')
        DIFY_API_KEY = getattr(settings, 'DIFY_API_KEY', {})
        
        api_key = DIFY_API_KEY.get(user_type)
        if not api_key:
            return JsonResponse({'error': 'API key not found for this user type'}, status=500)
        
        # 构建请求URL
        stop_url = f"{DIFY_STOP_API_URL}/{conversation_id}/stop-streaming"
        
        # 构建请求头
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 发送停止请求
        response = requests.post(stop_url, headers=headers, json={})
        
        if response.status_code != 200:
            logger.error(f"Dify API error: {response.text}")
            return JsonResponse({'error': f'Dify API error: {response.text}'}, status=response.status_code)
        
        logger.info("Stop response request sent successfully")
        return JsonResponse({'success': True}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        logger.error(f"Error in dify_stop_response: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
