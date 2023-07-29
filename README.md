# audio2vmd


## python 3.10

### 通常ターミナル
 1. `conda create -n audio2vmd pip python=3.10`
 1. `conda activate audio2vmd`

### 管理者権限付きターミナル

 1. `git submodule add -b develop https://github.com/miu200521358/mmd_base.git mmd_base`
 2. `mkdir src`
 3. `cd src`
 4. `mklink /D mlib ..\mmd_base\mlib`

### 通常ターミナル
 1. `pip install -r requirements.txt`
 1. `pip install -r mmd_base\requirements.txt`
 1. `pip install -r mmd_base\requirements_test.txt`
 1. `pip install --force click==7.1.2`


https://stackoverflow.com/questions/72356588/could-not-locate-zlibwapi-dll-please-make-sure-it-is-in-your-library-path
copied zlibwapi.dll to C:\Windows\System32 and C:\Windows\SysWOW64

