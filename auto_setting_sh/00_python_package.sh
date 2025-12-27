#!/bin/bash

# 준간에 실패하면 중단
set -e -o pipefail

#
sudo apt update && sudo apt upgrade -y

sudo apt install python3-picamera2 -y

# 패키지 whl파일 다운 <- zero2w는 cpu, ram 이 작기때문에 가상환경 사용 x
base_path=~/Zero2w_cam2ocr
err_log=~/Zero2w_cam2ocr/download_whl

cd $base_path

pip download -r $base_path/requirements.txt -d $base_path/download_whl --only-binary=:all: -v | tee $err_log/download_err.log

pip install --no-index --find-links="$base_path/download_whl" -r $base_path/requirements.txt -v | tee $err_log/install_err.log