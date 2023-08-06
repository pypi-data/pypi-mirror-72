const PaletteElement = class {
    static mInstance = null;
    mName = "PaletteElement";
    
    constructor(){
        if(!this.mInstance){
            this.mInstance = this;
        } 
        return this.mInstance;
    }

    static GetInstance = () => {
        return this.mInstance;
    }
    /* TODO:
        아래 3개의 메소드는 반드시 오버라이드해야 합니다.
    */
    GetName = () => {
        console.log("must override");
    }

    Render = () => {
        console.log("must override");
    }

    ExecuteCode = (str) => {
        console.log("must override");
    }
}

