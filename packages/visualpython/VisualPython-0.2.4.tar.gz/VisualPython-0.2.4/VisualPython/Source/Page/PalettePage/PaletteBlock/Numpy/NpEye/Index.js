define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpEye = class extends PaletteElement {
        static mInstance = null;
        mName = "NpEye";
        
        constructor(){
            super();
            if(!this.mInstance){
                this.mInstance = this;
            } 
            return this.mInstance;
        }

        static GetInstance = () => {
            return this.mInstance;
        }

        GetName = () => {
            return this.mName;
        }

        ExecuteCode = () => {
            let str = `arr = np.eye(3, dtype=int)\n`;
            str += `arr\n`;
            str += `arr = np.eye(4, k=1, dtype=float)\n`;
            str += `arr\n`;
            str += `arr = np.eye(5, k=-1, dtype=int)\n`;
            str += `arr`;
            SetCodeAndExecute(str);
        }
    }
    
    return new NpEye();
});
