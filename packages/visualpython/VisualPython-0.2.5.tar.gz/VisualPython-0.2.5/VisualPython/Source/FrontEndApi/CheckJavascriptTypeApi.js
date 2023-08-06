define([], function() {

    // 자식 클래스가 부모 클래스의 인스턴스 인지 확인하는 함수
    const CheckIsInstance = (childClass, parentClass) => {
        return childClass instanceof parentClass
    };
    
    // string인지 확인
    const CheckIsString = () => {
        return;
    };

    // Number인지 확인
    const CheckIsNumber = () => {
        return;
    };

    // Boolean인지 확인
    const CheckIsBoolean = () => {
        return;
    };

    // Null인지 확인
    const CheckIsNull = () => {
        return;
    };

    // Undefined인지 확인
    const CheckIsUndefined = () => {
        return;
    };

    // Symbol인지 확인
    const CheckIsSymbol = () => {
        return;
    };

     // Array인지 확인
    const CheckIsArray = () => {
        return;
    };

     // Object인지 확인
    const CheckIsObject = () => {
        return;
    };

    return {
        CheckIsInstance,

        CheckIsString,
        CheckIsNumber,
        CheckIsBoolean,
        CheckIsNull,
        CheckIsUndefined,
        CheckIsSymbol,
        CheckIsArray,
        CheckIsObject
    }
});