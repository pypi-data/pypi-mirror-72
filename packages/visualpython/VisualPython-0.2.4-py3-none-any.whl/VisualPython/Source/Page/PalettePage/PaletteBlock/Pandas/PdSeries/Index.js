define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdSeries = class extends PaletteElement {
        static mInstance = null;
        mName = "PdSeries";
        
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
            let str = `data = np.array(['a','b','c','d'])\n`;
            str += `s = pd.Series(data,index=[100,101,102,103])\n`;
            str += `s`;
            SetCodeAndExecute(str);
        }
    }
    
    return new PdSeries();
});
