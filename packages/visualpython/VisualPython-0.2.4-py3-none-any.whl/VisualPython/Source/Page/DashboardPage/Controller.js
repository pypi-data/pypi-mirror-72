define([


], function(  )
{
    /*
        // TODO:
        DashboardPage은 사용자가 차트 등으로 비주얼 파이썬 사용 내역과 템플릿 옵션을 간단히 볼 수 있게 만든 화면입니다.
        현재는 구현되지 않았습니다.

        모든 Page마다 Controller와 Model파일을 구분해놨습니다.
        Controller는 동적 page 렌더링과 page 태그에 매핑된 click 함수를 구현하고
        Model은 page에서 사용하는 데이터를 저장하기 위한 목적으로 만들었습니다.

        그러나 현재 Controller에만 구현한 상태입니다.
        추후에 Controller와 Model을 분리하거나 혹은 이방식이 복잡하다면 새로운 방법을 찾아 구현하겠습니다.
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
            console.log("DashboardPage");
        }
    }

    return new Controller();
})