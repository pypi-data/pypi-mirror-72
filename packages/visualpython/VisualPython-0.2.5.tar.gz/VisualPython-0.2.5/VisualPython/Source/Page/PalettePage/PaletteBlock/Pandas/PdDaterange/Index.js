define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdDaterange = class extends PaletteElement {
        static mInstance = null;
        mName = "PdDaterange";
        
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
            let str = `dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')\n`;
            str += `long_df = pd.DataFrame(np.random.randn(100, 4), index=dates,columns=['Colorado', 'Texas','New York', 'Ohio'])\n`;
            str += `long_df.loc['5-2001']`;
            SetCodeAndExecute(str);
        }
    }
    
    return new PdDaterange();
});
