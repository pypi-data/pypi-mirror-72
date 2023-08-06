define([


], function(  )
{
    /* TODO: SettingPage는 사용자가 비주얼 파이썬에서 옵션을 설정하는 화면입니다.
             아직 구체적인 옵션이 정해지지 않아 텅 빈 상태입니다.
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
            console.log("SettingPage");
        }
    }

    return new Controller();
})