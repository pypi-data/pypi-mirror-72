define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpFlip = class extends PaletteElement {
        static mInstance = null;
        mName = "NpFlip";
        
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
            let str = `arr = np.arange(5)\n`;
            str += `flipedArr = np.flip(arr)\n`;
            str += `print(flipedArr)`;

            SetCodeAndExecute(str);
        }
    }
    
    return new NpFlip();
});
