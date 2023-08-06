define([
    `nbextensions/VisualPython/Source/FrontEndApi/Index`,
    `nbextensions/VisualPython/Source/Page/PalettePage/PaletteBlock/PaletteElement`,
], function( 
    FrontEndApis
 ){
    const { SetCodeAndExecute } = FrontEndApis.JupyterNativeApi;
    const PdMap = class extends PaletteElement {
        static mInstance = null;
        mName = "PdMap";
        
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
            let str = `data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon','Pastrami', 'corned beef', 'Bacon','pastrami', 'honey ham', 'nova lox'],'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})\n`;
            str += `data\n`;
            SetCodeAndExecute(str);

            str = ``;
            str += `meat_to_animal = {'bacon': 'pig','pulled pork': 'pig','pastrami': 'cow','corned beef': 'cow','honey ham': 'pig','nova lox': 'salmon'}\n`;
            str += `lowercased = data['food'].str.lower()\n`;
            str += `lowercased\n`;
            SetCodeAndExecute(str);

            str = ``;
            str += `data['animal'] = lowercased.map(meat_to_animal)\n`;
            str += `data\n`;
            SetCodeAndExecute(str);
        }
    }
    
    return new PdMap();
});
