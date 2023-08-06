define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;

    const NpArange = class extends PaletteElement {
        static mInstance = null;
        mName = "NpArange";

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
            let str = `arr = np.arange(0,100,2)\n`;
            str += `print(arr)`;

            SetCodeAndExecute(str);
        }
    }
    
    return new NpArange();
});
