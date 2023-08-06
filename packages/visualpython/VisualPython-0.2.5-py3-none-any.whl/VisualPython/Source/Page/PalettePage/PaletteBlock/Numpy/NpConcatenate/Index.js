define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpConcatenate = class extends PaletteElement {
        static mInstance = null;
        mName = "NpConcatenate";
        
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
            let str = `arr1 = np.array([1,2,3,4,5,6,7,8,9])\n`;
            str += `arr2 = np.arange(0,100,2)\n`;
            str += `arr3 = np.concatenate([arr1,arr2], axis=0)\n`;
            str += `print(arr3)`;

            SetCodeAndExecute(str);
        }
    }
    
    return new NpConcatenate();
});
