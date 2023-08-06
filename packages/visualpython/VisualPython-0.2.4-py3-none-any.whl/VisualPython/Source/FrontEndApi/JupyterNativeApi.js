define([
    `nbextensions/VisualPython/Source/ConstData/ConstString/Index`,
], function(
    ConstString
) {
    const { STR_SCANDIR } = ConstString;
    /*
        코드를 주피터 셀에 실행하는 함수다.
    */
    const SetCodeAndExecute = (str) => {
        Jupyter.notebook.
            insert_cell_above('code').
            set_text(str);
        Jupyter.notebook.select_prev();
        Jupyter.notebook.execute_cell_and_select_below();
    }
    
    /*
        focus하면 주피터 핫키가 disable되고
        blur하면 주피터 핫키가 enable된다.

        input태그에 값을 입력할 때 사용한다.
    */
    const FocusInputDisableAndBlurEnable = (tagSelector) => {
        $(tagSelector).on('focus', () => {
            Jupyter.notebook.keyboard_manager.disable();
        });

        $(tagSelector).on('blur', () => {
            Jupyter.notebook.keyboard_manager.enable();
        });
    }

    /*
        주피터 커널에 파이썬 코드를 실행하는 함수. 비동기.
        현재 디렉토리 목록을 검색하는 파이썬 코드를 실행한다.
    */
    const ExecuteAtJupyterKernelCurrDir = (callback) => {
        Jupyter.notebook.kernel.execute(
            STR_SCANDIR
            , {
                iopub: {
                    output: function (msg) {
                        const currentDirStr = msg.content.text;
                        callback(currentDirStr);
                    }
                }
            }
            , { silent: false }
        );
    }
    
    /*
        주피터 커널에 파이썬 코드를 실행하는 함수. 비동기.
        상위 디렉토리를 검색하는 파이썬 코드를 실행한다.
    */
    const ExecuteAtJupyterKernelBeforeDir = (callback) => {
        const cmdCdBeforeStr = `%cd ..`;
        Jupyter.notebook.kernel.execute(
            cmdCdBeforeStr
            , {
                iopub: {
                    output: function () {
                        callback();
                    }
                }
            }
            , { silent: false }
        );
    }
    
    /*
        주피터 커널에 파이썬 코드를 실행하는 함수. 비동기.
        특정 폴더 디렉토리 목록을 검색하는 파이썬 코드를 실행한다.
    */
    const ExecuteAtJupyterKernelToDir = (destDir, callback) => {
        const cmdCdToDirStr = `%cd ${destDir}`;
        Jupyter.notebook.kernel.execute(
            cmdCdToDirStr
            , {
                iopub: {
                   output: function () {
                        callback();
                    }
                }
            }
            , { silent: false }
        );
    }

    /*
        주피터 커널에 파이썬 코드를 실행하는 함수. 비동기.
        현재 디렉토리 path 정보를 불러오는 파이썬 코드를 실행한다.
    */
    const ExecuteAtJupyterKernelPwd = (callback) => {
        const cmdPwdString = `%pwd`;
        Jupyter.notebook.kernel.execute(
            cmdPwdString
            , {
                iopub: {
                    output: function (msg) {
                        const currentPath = msg.content.data['text/plain'];
                        callback(currentPath);
                    }
                }
            }
            , { silent: false }
        );
    }
    
    /*
        주피터 커널에 파이썬 코드를 실행하는 함수. 비동기.
        dirObj옵션에 따라 다양한 디렉토리 정보를 불러오는 파이썬 코드를 실행한다.

        @param dirObj 파라미터는 
                { 
                    direction, 
                    destDir 
                } 
                객체 형식으로 구성되어 있다.
                
                direction은 "prev", "to", "before", "init" 4가지이며
                destDir은 direction이 "prev" "to" 일 때만,지정할 수 있다.
    */
    const ExecuteAtJupyterKernelSetDir = (dirObj, callback) => {
        const { direction } = dirObj;
        if(direction === "to" || direction === "prev"){
            const { destDir } = dirObj;
            ExecuteAtJupyterKernelToDir(destDir, callback);
        } else if(direction === "before"){
            ExecuteAtJupyterKernelBeforeDir(callback);
        } else {
            callback();
        }
    }
    
    return {
        SetCodeAndExecute,
        FocusInputDisableAndBlurEnable,

        ExecuteAtJupyterKernelSetDir,

        ExecuteAtJupyterKernelCurrDir,
        ExecuteAtJupyterKernelBeforeDir,
        ExecuteAtJupyterKernelToDir,
        ExecuteAtJupyterKernelPwd,
    }
});