
define([
    
], function() {

    // dom을 생성하는 함수
    const CreateDom = (tagSelector) => {
        return document.createElement(tagSelector);
    }

    // 특정 dom을 가져오는 함수
    const GetDom = (tagSelector) => { 
        return document.querySelector(tagSelector);
    }

    // 특정 dom list를 가져오는 함수
    const GetDomList = (tagSelector) => { 
        return document.querySelectorAll(tagSelector);
    }

    // 특정 dom의 높이 값을 가져오는 함수
    const GetDomHeight = (tagSelector) => {
        const clientHeight = document.querySelector(tagSelector).offsetHeight;
        return clientHeight;
    }

    // 사용자 정의 dom을 생성하는 함수
    /*
        MakeDom함수 예제
        MakeDom("div", { innerHTML:"안녕하세요"});
            -> <div>​안녕하세요</div>​
        
        MakeDom("div", { classList:"white",
                        innerHTML:"안녕하세요" });
            -> <div class=​"white">안녕하세요​</div>​

        MakeDom("div", { onclick:function() {console.log(1);} ,
                         innerHTML:"안녕하세요",
                         classList:"white"  
                        });
            -> <div class=​"white" onclick>​안녕하세요</div>​
    */
    const MakeDom = (tagSelector, attribute = {}) => {
        const dom = Object.entries(attribute).reduce((element, value) => {
            typeof element[value[0]] === 'function' 
                            ? element[value[0]](value[1]) 
                            : (element[value[0]] = value[1]);
            return element;
        }, document.createElement(tagSelector));

        return dom;
    }

    return {
        CreateDom,
        GetDom,
        GetDomList,
        GetDomHeight,
        
        MakeDom
    }
});
