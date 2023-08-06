define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const NpFlatten = class extends PaletteElement {
        static mInstance = null;
        mName = "NpFlatten";
        
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
            let str = `arr = np.array( [ (1,7,3,4),(3,2,4,1) ] )\n`;
            str += `print(arr)`;
            SetCodeAndExecute(str);
            
            str = ``;
            str += `arr2 = arr.flatten()\n`;
            str += `print(arr2)`;
            SetCodeAndExecute(str);
        }
    }
    
    return new NpFlatten();
});
