define([


], function(  )
{
    /* TODO:
        MyTemplatePage은 사용자가 만든 템플릿을 저장하고 볼 수 있는 화면입니다.
        코드를 만드는 기능, 모듈이 정해지고 나면 이후에 구현할 화면입니다.
    */
    const Controller = class {
        static mInstance = null;

        constructor(){
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        Init = () => {
            console.log("MyTemplatePage");
        }
    }

    return new Controller();
})