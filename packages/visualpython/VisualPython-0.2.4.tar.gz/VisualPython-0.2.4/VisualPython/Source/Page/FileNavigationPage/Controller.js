define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Component/Index`,
], function( 
    FrontEndApis,
    
    Component
){
    // 현재 js파일에서 사용할 api, config 값 불러옴
 
    const { ParseCurrentDirPathString } = FrontEndApis.ParserApi;
    const { GetDom, CreateDom, MakeDom } = FrontEndApis.DocumentObjectModelApi;
    const { ExecuteAtJupyterKernelCurrDir,
            ExecuteAtJupyterKernelToDir,
            ExecuteAtJupyterKernelPwd,

            ExecuteAtJupyterKernelSetDir } = FrontEndApis.JupyterNativeApi;

    const { RenderLoadingBar, RenderAlertModal, RenderYesOrNoModal } = Component;

    /* TODO:
        FileNavigationPage은 서버를 통해 파일 디렉토리 path를 찾는 화면입니다.
        현재는 csv만 import가능하게 구현했습니다.

        모든 Page마다 Controller와 Model파일을 구분해놨습니다.
        Controller는 동적 page 렌더링과 page 태그에 매핑된 click 함수를 구현하고
        Model은 page에서 사용하는 데이터를 저장하기 위한 목적으로 만들었습니다.

        그러나 현재 Controller에만 구현한 상태입니다.
        추후에 Controller와 Model을 분리하거나 혹은 이방식이 복잡하다면 새로운 방법을 찾아 구현하겠습니다.
    */
    const FileNavigationController = class {
        static mInstance = null;

        mBaseDirStr = '';
        mBaseFileStr = '';

        mCurrentDirStr = '';
        mCurrentFileStr = '';

        mDirHistoryStack = [];

        // 이 클래스는 싱글톤
        constructor(){
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        GetInstance = () => {
            return this;
        }

        // 기본 디렉토리 path를 가져온다
        getBaseDirStr = () => {
            return this.mBaseDirStr;
        }

        // 기본 디렉토리 path를 변경한다
        setBaseDirStr = (baseDirStr) => {
            this.mBaseDirStr = baseDirStr;
        }

        // 현재 디렉토리 path를 가져온다
        getCurrentDirStr = () => {
            return this.mCurrentDirStr;
        }
        // 현재 디렉토리 path를 변경한다
        setCurrentDirStr = (currentDirStr) => {
            this.mCurrentDirStr = currentDirStr;
        }
        // 이전 디렉토리 검색 history를 담은 stack을 가져온다
        getDirHistoryStack = () => {
            return this.mDirHistoryStack;
        }
        
        // 이전 디렉토리 검색 history를 담은 stack에 디렉토리 정보를 push하는 함수
        /*
            @param: Object { prev, next }
            예시1 : {
                        prev: C:\\Users\\L.E.E\\Desktop\\Bit Python,
                        next: C:\\Users\\L.E.E\\Desktop,
                    }
        */
        pushDirHistoryStack = (dirInfo) => {
            this.mDirHistoryStack.push(dirInfo);
        }

        //  디렉토리 검색 history를 담은 stack에 디렉토리 정보를 pop하는 함수
        popDirHistoryStackAndGetPopedData = () => {
            if(this.mDirHistoryStack.length < 1) {
                return;
            }
            return this.mDirHistoryStack.pop();
        }

        // 디렉토리 검색 history를 담은 stack을 리셋하는 함수
        resetStack = () => {
            this.mDirHistoryStack = [];
        }
        
        // Visual python 초기 렌더링시 실행되는 init 함수
        Init = () => {

            ExecuteAtJupyterKernelPwd((currentDirStr) => {
                const slicedCurrentDirStr = currentDirStr.slice(1, currentDirStr.length -1);
                this.setBaseDirStr(slicedCurrentDirStr);
            });
            
            // FileNavigationPage 파일네비게이션 페이지를 html에 렌더링하는 함수.
            // html load이후 파일네비게이션에 필요한 click함수를 매핑시킨다, 
            // 사용자가 파일네비게이션을 열면 현재 디렉토리 정보로 초기 렌더링(line 124: this.Render)을 실시한다.
            $(`<div class="FileNavigationPage hide"></div>`)
                .load(Jupyter.notebook.base_url + "nbextensions/VisualPython/Source/Page/FileNavigationPage/Index.html", 
                     (response, status, xhr) => {

                        /* FIXME: 
                            // 처음 FIND CSV 파일네비게이션 열었을때 실행

                            특정 cssClass인 hide로 display none을 하면 html에 보이진 않지만, 메모리는 여전히 할당상태로 알고 있습니다.
                            removeChild를 하면 완전히 사라집니다.
                        */
                        const btnFindCsv = GetDom(".btn-find-csv");
                        btnFindCsv.addEventListener('click', () => {
                            if($('.FileNavigationPage').hasClass("hide")){
                                $('.FileNavigationPage').removeClass("hide");
                                $('.FileNavigationPage').addClass("show");
                              
                                this.initRender();

                            } else{
                                $('.FileNavigationPage').addClass("hide");
                                $('.FileNavigationPage').removeClass("show");
                            }
                        });

                        // 파일네비게이션을 닫았을때 실행되는 click 함수
                        $('.directoryComponent-closedBtn').click(() => {
                            ExecuteAtJupyterKernelToDir(this.getBaseDirStr(), () => {
                                this.resetStack();
                                $('.directoryComponent-container').empty();
                                $('.FileNavigationPage').addClass("hide");
                                $('.FileNavigationPage').removeClass("show");
               
                            });
                        });

                        // 상위 디렉토리 클릭시 실행되는 함수
                         $('.directoryComponent-btn-up').click(() => {
                                        
                             ExecuteAtJupyterKernelPwd((currentDirStr) => {
                                const slicedCurrentDirStr = currentDirStr.slice(1, currentDirStr.length -1);

                                if (slicedCurrentDirStr === this.getBaseDirStr()){
                                    RenderAlertModal('기본 디렉토리보다 상위로 검색할 수 없습니다');
                                    return;
                                }

                                this.startLoadingBar();

                                // 현재 디렉토리 path보다 상위 디렉토리를 검색
                                const dirObj = {
                                    direction: "before",
                                }
                                this.executeKernelToDir(dirObj);
                            });
                        });

                        // 이전 디렉토리 검색 클릭시 실행되는 함수
                        $('.directoryComponent-btn-prev').click(() => {
                            if(this.getDirHistoryStack().length === 0){
                                RenderAlertModal('이전 디렉토리 검색 목록이 없습니다');
                                return;
                            }
                            // 이전 디렉토리 history stack 목록을 뒤져서,
                            // 가장 최근에 다녀간 이전 디렉토리로 검색
                            const popedData = this.popDirHistoryStackAndGetPopedData();
                            const dirObj = {
                                direction: "prev",
                                destDir: popedData.prev
                            }
                            this.executeKernelToDir(dirObj);              
                        });

                    }).appendTo('.MainContainer-body');
        }

        // Init 함수 이후 사용자가 파일네비게이션을 열면 FileNavigationPage가 보인다음 실행되는 함수
        initRender = () => {
            const dirObj = {
                direction: "init",
            }
            this.executeKernelToDir(dirObj);
        }

        // 파싱된 자바스크립트 배열 디렉토리정보를 파일네비게이션 page에 렌더링하는 함수 
        /* 
            @param 1 Array< Object {name, type} > 
            @param 2 string

            @return void
        */
        // 폴더 디렉토리는 makeFolderDom함수로 만들고
        // 파일 디렉토리는 makeFileDom함수로 만든다
        renderCurrentDirPathInfo = (dirInfoArr, rootFolderName) => {
            $('.directoryComponent-container').empty();
    
            const currentDirRootDom = $(`<ul class="directoryComponent-ul">
                                            <li class="directoryComponent-li root folder-has-childrenfolder">
                                                <span class="directoryComponent-column">
                                                    <span class="icon-tree-down"></span>
                                                    <span class="directoryComponent-dir-text icon-folder"> 
                                                        ${rootFolderName}
                                                    </span>
                                                </span>
                                            </li>
                                         </ul>`);
        
            const folderArr = [];
            const fileArr = [];
        
            let nodeInfo = { name:"", 
                             type:"" };
            // 디렉토리 정보가 담긴 자바스크립트 배열 dirInfoArr을 index 0부터 1씩 늘려가면서
            // 폴더인지 파일인지 확인후 html 태그를 만든다. 
            let index = 0;
            while(index < dirInfoArr.length){
                nodeInfo = dirInfoArr[index];
                let tempDom = null;
                // 디렉토리 정보가 폴더 일 경우
                if(nodeInfo.type === "dir"){
                    tempDom = this.makeFolderDom(nodeInfo);
                    folderArr.push(tempDom);
                } else {
                // 디렉토리 정보가 파일 일 경우
                    tempDom = this.makeFileDom(nodeInfo);
                    fileArr.push(tempDom);
                }
        
                index++;
            }
            
            currentDirRootDom.appendTo('.directoryComponent-container');
            const directoryComponentUl = $('.directoryComponent-ul');
            folderArr.forEach(dom => {
                directoryComponentUl.append(dom);
            });
            fileArr.forEach(dom => {
                directoryComponentUl.append(dom);
            });
        }
        /* FIXME: 
            <div/> 형식의 폴더 디렉토리를 만드는 함수 
            바닐라 자바스크립트로 dom을 구현했는데, 제이쿼리로 바꾸겠습니다.
        */
        makeFolderDom = (node) => {
            const folderName = node.name;

            const directoryLi = MakeDom("li" ,{
                classList: "directoryComponent-li"
            });
            const directorySpan = MakeDom("span" ,{
                classList: "directoryComponent-column"
            });
            const directorySpanDir = MakeDom("span" , {
                innerHTML: `${folderName}`,
                classList: "directoryComponent-dir-text icon-folder"
            });

            directorySpanDir.addEventListener('click', () => {

                this.deleteForderBtn();
                const button = MakeDom("button" , {
                    innerHTML: "폴더 이동",
                    classList: "directoryComponent-btn-move-to-folder",
                    value: `${folderName}`
                });

                button.addEventListener("click", () => {
                    $('.directoryComponent-container').empty();

                    const dirObj = {
                        direction: "to",
                        destDir: folderName
                    }
                    this.executeKernelToDir(dirObj);
                });

                directorySpanDir.appendChild(button);
   
            });

            directoryLi.appendChild(directorySpan.appendChild(directorySpanDir));
                
            return directoryLi;
        }
        /* FIXME: 
            <div/> 형식의 파일 디렉토리를 만드는 함수 
            바닐라 자바스크립트로 dom을 구현했는데, 제이쿼리로 바꾸겠습니다.
        */
        makeFileDom = (node) => {
            const fileName = node.name;

            const directoryLi = MakeDom("li" ,{
                classList: "directoryComponent-li"
            });
            const directorySpan = MakeDom("span" ,{
                classList: "directoryComponent-column directoryComponent-dir-text icon-file",
                innerHTML: `${fileName}`
            });

            directorySpan.addEventListener("click", () => {
         
                this.deleteFileBtn();
                const button = MakeDom("button" , {
                    innerHTML: "파일 선택",
                    classList: "directoryComponent-btn-select-file",
                    value: `${fileName}`
                });

                button.addEventListener("click", () => {
                    const dirPath = $(".directoryComponent-directory-nowLocation").html().trim();
                    if(fileName.indexOf(".csv") === -1) {
                        RenderAlertModal('csv 파일이 아닙니다');
                        return;
                    }
                    const baseDirStr = this.getBaseDirStr();
         
                    RenderYesOrNoModal(dirPath, fileName, baseDirStr);

                    this.resetStack();
                });

                directorySpan.appendChild(button);
            });

            directoryLi.appendChild(directorySpan);
            return directoryLi;
        }

        // loadingBar를 생성합니다.
        startLoadingBar = () => {
            $('.directoryComponent-container').empty();
            RenderLoadingBar();
        }
    
        // loadingBar를 종료합니다.
        finishLoadingBarAndSetCurrDirStr = (currentDirStr) => {
            this.setCurrentDirStr(currentDirStr);
            $('.directoryComponent-container').find('.loadingBar').remove();
            $(".directoryComponent-directory-nowLocation").html(currentDirStr);
        }

        // 폴더 이동 버튼을 삭제합니다
        deleteForderBtn = () => {
            $('.icon-folder').each(function() {
                $(this).find(".directoryComponent-btn-move-to-folder").remove();    
            });
        }

        // 파일 선택 버튼을 삭제합니다.
        deleteFileBtn = () => {
            $('.icon-file').each(function() {
                $(this).find(".directoryComponent-btn-select-file").remove();    
            });
        }

        /* 파이썬 커널에서
            1. 디렉토리 정보 string으로 받아옴 
                이 함수가 디렉토리를 찾는 가짓수는 총 4가지
                before 상위 디렉토리 검색
                to 특정 폴더 디렉토리 검색
                prev 이전 디렉토리 검색
                init 파일네비게이션 처음 시작할 때 기본 디렉토리 검색
            2. pwd명령어로 디렉토리 path string 받아옴
            3. 2에서 받아온 string 정보를 자바스크립트 객체로 파싱
            4. 파싱된 객체정보를 <div/> 형식으로 바꿔 화면에 동적 렌더링
        */
        executeKernelToDir = (dirObj) => {
            this.startLoadingBar();

            ExecuteAtJupyterKernelSetDir(dirObj , () => {
                ExecuteAtJupyterKernelCurrDir((result) => {
                    ExecuteAtJupyterKernelPwd((currentDirStr) => {
                        const dirInfoArr = ParseCurrentDirPathString(result);
                        const slicedCurrentDirStr = currentDirStr.slice(1, currentDirStr.length -1);
                        const splitedDirStrArr = slicedCurrentDirStr.split('\\');
                        const rootFolderName = splitedDirStrArr[splitedDirStrArr.length - 1];

                        if(dirObj.direction === "before" || dirObj.direction === "to"){
                            const dirObj = {
                                prev: this.getCurrentDirStr(),
                                next: slicedCurrentDirStr
                            }
                            this.pushDirHistoryStack(dirObj);
                        }

                        this.finishLoadingBarAndSetCurrDirStr(slicedCurrentDirStr);
                        this.renderCurrentDirPathInfo(dirInfoArr ,rootFolderName );   
                    });
                });
            });
        }
    }

    return new FileNavigationController();
})