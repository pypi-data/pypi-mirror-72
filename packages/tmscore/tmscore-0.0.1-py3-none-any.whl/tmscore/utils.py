# -*- coding: utf-8 -*-
"""
Created on 2020/6/29

@author: yang.zhou
"""

import os
import subprocess
from subprocess import CalledProcessError

import shutil
import logging

from datetime import datetime

# 启用日志打印
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def path_pre_check(cmd):
    """
    path不能为空,'/' ,'/*' ,'\','\*'
    """
    path_list = []

    for t in cmd.split():
        if t in ['tar']:
            return cmd
        if t in ['rm']:
            continue
        if t[0] == '-':
            continue
        path_list.append(t)

    for path in path_list:
        logger.debug("开始命令路径预检查.")
        if not path or path in ['/', '/*', '//', '//*', '\\', '\\*']:
            raise Exception("The path to be deleted cannot be empty or '/'!")
    else:
        logger.debug("检查完毕, 执行路径未包含危险路径.")
    return cmd


def with_system(cmd):
    logger.debug('cmd: %s', cmd)
    os.system(path_pre_check(cmd))


def with_mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        logger.info("文件夹已存在，删除文件夹重新创建: %s", path)
        try:
            shutil.rmtree(path_pre_check(path))
            os.makedirs(path)
        except Exception:
            raise
        else:
            logger.info("mkdir {} success!".format(path))
    else:
        logger.info("mkdir {} success!".format(path))


def with_rmtree(path, ignore_errors=False, onerror=None):
    if os.path.exists(path):
        logger.debug('rm %s', path)
        shutil.rmtree(path_pre_check(path), ignore_errors, onerror)


def with_copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def with_copy(src, dst, version=1):
    if os.path.isdir(src):
        with_copytree(src, dst)
        return
    if os.path.isdir(dst):
        dst_root = dst
    else:
        dst_root = os.path.dirname(dst)

    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    logger.info("Start cp file, %s==>%s.", src, dst)

    if version == 1:
        shutil.copy(src, dst)
    else:
        shutil.copy2(src, dst)


def with_popen(cmd, msg_on=True):
    logger.info('Execute command: %s', cmd)
    process = subprocess.Popen(path_pre_check(cmd), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = get_str_code(stdout), get_str_code(stderr)
    if process.returncode:
        if msg_on:
            logger.error('CalledProcessError:\n%s', stdout+stderr)
        raise CalledProcessError(process.returncode, cmd, stdout+stderr, stderr)
    if msg_on:
        logger.info('stdout:\n%s', stdout)
    return stdout


def with_output(cmd):
    logger.info('Execute command: %s', cmd)
    return get_str_code(subprocess.check_output(path_pre_check(cmd), shell=True))


def with_call(cmd):
    logger.info('Execute command: %s', cmd)
    subprocess.check_call(path_pre_check(cmd), shell=True)


def get_str_code(std: bytes):
    codec = ['utf8', 'gbk']
    for code in codec:
        try:
            return std.decode(code)
        except UnicodeDecodeError:
            continue
        except AttributeError:
            return std


def with_scp(local_path, remote_ip, remote_path):
    """
    scp命令
    :param remote_ip:
    :param local_path:
    :param remote_path:
    :return:
    """
    logger.info("执行scp.")
    scp_cmd = 'scp -r {local_path} {username}@{host}:{remote_path}'
    with_system(scp_cmd.format(local_path=local_path, username='tomcat', host=remote_ip, remote_path=remote_path))


def parse_argv(arg):
    if len(arg) == 5:
        arg.insert(4, None)
    return arg[1:]


def get_sysdate():
    """
    返回当前时间格式,如yymmddhhmmss
    :return:
    """
    return datetime.today().strftime('%Y.%m.%d.%H.%M.%S')


def datetime_now():
    """
    返回当前时间
    :return:
    """
    return datetime.now()


def get_sysdate_file():
    """
    返回当前时间格式,如yymmddhhmmss
    :return:
    """
    return datetime.today().strftime('%Y%m%d')
