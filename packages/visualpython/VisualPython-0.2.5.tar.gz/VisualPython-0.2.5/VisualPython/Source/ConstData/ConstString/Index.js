
define([

], 
function() {

    // 파이썬 커널에서 현재 디렉토리 정보를 가져오는 코드
    // 이 코드를 커널에 실행시키면서 파일 네비게이션을 구현
    let STR_SCANDIR = `import os\n`
    STR_SCANDIR += `with os.scandir() as i:\n`
    STR_SCANDIR += `   info = []\n`
    STR_SCANDIR += `   for entry in i:\n`
    STR_SCANDIR += `       type = 'other'\n`
    STR_SCANDIR += `       if entry.is_file():\n`
    STR_SCANDIR += `          type = 'file'\n`
    STR_SCANDIR += `       elif entry.is_dir():\n`
    STR_SCANDIR += `          type = 'dir'\n`
    STR_SCANDIR += `       info.append({'name':entry.name, 'type':type})\n`
    STR_SCANDIR += `   print(info)\n`;

    return {
        STR_SCANDIR
    }
});