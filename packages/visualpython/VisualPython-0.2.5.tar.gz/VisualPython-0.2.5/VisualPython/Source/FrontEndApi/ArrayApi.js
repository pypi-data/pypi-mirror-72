define([], function() {


    // 파라미터로 들어온 lengthNumber만큼 배열안에 0부터 더미 숫자를 만들어 리턴하는 함수
    const MakeDummyNumberArray = (lengthNumber) => {
        return Array.from({ lengthNumber }, (_, i) => 0 + i);
    };

    // 1차원 배열을 2차원 배열로 변환해주는 함수
    /*
        @param1 1차원 배열
        @param2 1차원 배열의 length
        @param3 2차원 배열로 변환시 2차원 배열의 각 요소는 1차원 배열이다. 이 1차원 배열의 갯수(length)를 지정하는 파라미터다.

        @return 2차원 배열
    */

    const MapOneArrayToDoubleArray = ( oneDimensionArray, 
                                       showDataCountNumber, 
                                       columnNumber ) => {
        const doubleArray = [];
        let tempArray = [];

        for (let i = 0; i < showDataCountNumber; i++){
            if (i !== 0 && i % columnNumber === 0){
                doubleArray.push(tempArray);
                tempArray = [];
            }
            tempArray.push(oneDimensionArray[i]);
        }
        
        doubleArray.push(tempArray);

        return doubleArray;
    };

    return {
        MakeDummyNumberArray,
        MapOneArrayToDoubleArray
    }
});