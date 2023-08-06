define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpReshape = class extends PaletteElement {
        static mInstance = null;
        mName = "NpReshape";
        
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
            let str = `arr = np.linspace(1.0, 100.0, num=100)\n`;
            str += `arr.reshape(4,25,order='C')\n`;
            str += `print(arr)`;

            SetCodeAndExecute(str);
        }
    }
    
    return new NpReshape();
});
