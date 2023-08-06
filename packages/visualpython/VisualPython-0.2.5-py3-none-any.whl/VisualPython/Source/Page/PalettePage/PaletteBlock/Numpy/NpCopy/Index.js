define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpCopy = class extends PaletteElement {
        static mInstance = null;
        mName = "NpCopy";
        
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
            let str = `arr = np.arange(10)\n`;
            str += `print(arr)`;
            SetCodeAndExecute(str);

            str = '';
            str += `copy = arr[0:5].copy()\n`;
            str += `copy`;
            SetCodeAndExecute(str);
        }
    }
    
    return new NpCopy();
});
