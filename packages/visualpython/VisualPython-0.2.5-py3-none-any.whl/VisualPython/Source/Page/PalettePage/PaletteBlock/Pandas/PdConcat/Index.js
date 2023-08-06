define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdConcat = class extends PaletteElement {
        static mInstance = null;
        mName = "PdConcat";
        
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
            let str = `df_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],'B': ['B0', 'B1', 'B2'],'C': ['C0', 'C1', 'C2'],'D': ['D0', 'D1', 'D2']},index=[0, 1, 2])\n`;
            str += `df_2 = pd.DataFrame({'A': ['A3', 'A4', 'A5'],'B': ['B3', 'B4', 'B5'],'C': ['C3', 'C4', 'C5'],'D': ['D3', 'D4', 'D5']},index=[3, 4, 5])\n`;
            str += `df_1\n`;
            SetCodeAndExecute(str);
            str = ``;
            str += `df_2\n`;
            SetCodeAndExecute(str);
            str = ``;
            str += `df_12 = pd.concat([df_1, df_2])\n`;
            str += `df_12`;
            SetCodeAndExecute(str);
        }
    }
    
    return new PdConcat();
});
