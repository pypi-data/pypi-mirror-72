define([
    "base/js/namespace",
],  function() {
    
    /* TODO: 디폴트로 시스템 정보가 필요하다고 생각해서 만들었습니다.
             시스템정보는 Visual Python 초기 렌더링시 MainController가 불러옵니다.
             그리고 PalettePageController가 PalettePage의 pageModel 데이터들을 받아 함수 버튼들을 렌더링합니다.
             지금은 버튼을 누르면 하드코딩된 코드가 실행되지만,
             앞으로는 함수별로 옵션을 바꾸고 사용자 용도에 맞게 코드를 generate 할 수 있는 화면을 만들어야 합니다.
             이 때 필요한 정보들을 미리 객체 형식으로 만들어 놓고 불러다가 쓰면 좋을 것 같습니다.
    */ 
    const SystemData = {
        projectName: "Visual Python",

        pageList: [
            {
                pagename: "PalettePage",
                pageModel : {
                    baseLibrary: {
                        baseLibrary: {
                            name: "BaseLibrary",
                            cssClassName:"import-standard-library",
                            tagValue:"Import baseLibrary",
                        }
                    },
                    csv: {
                        findCsv: {
                            name: "FindCsv",
                            cssClassName:"btn-find-csv",
                            tagValue:"Find csv"
                        }
                    },
                    numpy: {
                        npArray:{
                            name: "NpArray",
                            cssClassName:"np-array",
                            tagValue:"np.array"
                        },
                        npArange: {
                            name: "NpArange",
                            cssClassName:"np-arange",
                            tagValue:"np.arange"
                        },
                        npConcatenate: {
                            name: "NpConcatenate",
                            cssClassName:"np-concatenate",
                            tagValue:"np.concatenate"
                        },
                        npFlip: {
                            name: "NpFlip",
                            cssClassName:"np-flip",
                            tagValue:"np.flip"
                        },
                        npReshape: {
                            name: "NpReshape",
                            cssClassName:"np-reshape",
                            tagValue:"np.reshape"
                        },
                        npZeros: {
                            name: "NpZeros",
                            cssClassName:"np-zeros",
                            tagValue:"np.zeros"
                        },
                        npOnes: {
                            name: "NpOnes",
                            cssClassName:"np-ones",
                            tagValue:"np.ones"
                        },
                        npEmpty: {
                            name: "NpEmpty",
                            cssClassName:"np-empty",
                            tagValue:"np.empty"
                        },
                        npFull: {
                            name: "NpFull",
                            cssClassName:"np-full",
                            tagValue:"np.full"
                        },
                        npIdentity: {
                            name: "NpIdentity",
                            cssClassName:"np-identity",
                            tagValue:"np.identity"
                        },
                        npEye: {
                            name: "NpEye",
                            cssClassName:"np-eye",
                            tagValue:"np.eye"
                        },
                        npTranspose: {
                            name: "NpTranspose",
                            cssClassName:"np-transpose",
                            tagValue:"np.transpose"
                        },
                        npCopy: {
                            name: "NpCopy",
                            cssClassName:"np-copy",
                            tagValue:"np.copy"
                        },
                        npFlatten: {
                            name: "NpFlatten",
                            cssClassName:"np-flatten",
                            tagValue:"np.flatten"
                        },
                        npRavel: {
                            name: "NpRavel",
                            cssClassName:"np-ravel",
                            tagValue:"np.ravel"
                        },
                    },
                    pandas: {
                        pdDataFrame: {
                            name: "PdDataFrame",
                            cssClassName:"pd-DataFrame",
                            tagValue:"pd.DataFrame"
                        },
                        pdDaterange: {
                            name: "PdDaterange",
                            cssClassName:"pd-date_range",
                            tagValue:"pd.date_range"
                        },
                        pdMap: {
                            name: "PdMap",
                            cssClassName:"pd-map",
                            tagValue:"pd.map"
                        },
                        pdMerge: {
                            name: "PdMerge",
                            cssClassName:"pd-merge",
                            tagValue:"pd.merge"
                        },
                        pdSeries: {
                            name: "PdSeries",
                            cssClassName:"pd-Series",
                            tagValue:"pd.Series"
                        },
                        pdConcat: {
                            name: "PdConcat",
                            cssClassName:"pd-concat",
                            tagValue:"pd.concat"
                        }
                    }
                }
            },
            {
                pagename: "DashboardPage",
                pageModel: {

                },
                CssClassName_body: "",
                CssClassName_nav_li: ""
            },
            {
                pagename: "MyTemplatePage",
                pageModel: {
                    
                },
                CssClassName_body: "",
                CssClassName_nav_li: ""
            },
            {
                pagename: "SettingPage",
                pageModel: {
                    
                },
                CssClassName_body: "",
                CssClassName_nav_li: ""
            }
        ]
    }

    return SystemData;
});
