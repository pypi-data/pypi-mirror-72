define([

], function() {

    const ParseJSON = (str) => {

    }

    const ParseJSobject = (str) => {

    }

    const ParseJupyterOneCell = (const_cellIndexNum, str) => {
        
    }

    const ParseJupyterAllCell = () => {
        
    }

    // 현재 디렉토리 path의 string을 자바스크립트 객체로 파싱하는 함수
    const ParseCurrentDirPathString = string => {
        const return_stacks = [];
        let cursor = 0;

        while(cursor < string.length){
            if(string[cursor] == `[`){
                cursor++;
            }
            if(string[cursor] == `{`){
                cursor++;
                cursor++;

                // name header
                string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));
                cursor++;
                string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));
                cursor++;

                // name string value
                const name = string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));

                cursor++;
                string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));

                //type header
                string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));
                cursor++;
                string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));
                cursor++;

                // type string value
                const type = string.substring(cursor, cursor = string.indexOf(`'`, cursor + 1));
                const node = { name, 
                               type };
                return_stacks.push(node);
                cursor++;
            }
            if(string[cursor] == `}`){
                cursor++;
            }
            if(string[cursor] == `]`){
                break;
            }
            cursor++;
        }
        return return_stacks;
    }

    return {
        ParseJSON,
        ParseJSobject,

        ParseJupyterOneCell,
        ParseJupyterAllCell,
        ParseCurrentDirPathString
    }
});