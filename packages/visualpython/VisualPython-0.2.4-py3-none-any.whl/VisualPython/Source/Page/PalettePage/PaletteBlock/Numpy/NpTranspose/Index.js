define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpTranspose = class extends PaletteElement {
        static mInstance = null;
        mName = "NpTranspose";
        
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
            let str = `arr = np.arange(15).reshape(3, 5)\n`;
            str += `print(arr)\n`;
            str += `arr.T`;
      
            SetCodeAndExecute(str);
        }
    }
    
    return new NpTranspose();
});
