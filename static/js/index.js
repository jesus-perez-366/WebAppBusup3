// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

$(function () {
        
    
    
    





    var reportContainer = $("#report-container").get(0);
    console.log(reportContainer)

    // Initialize iframe for embedding report
    powerbi.bootstrap(reportContainer, { type: "report" });
    var models = window["powerbi-client"].models;
        // aca se define la constante que tiene el valor de los filtro  para mas info consultar
    
    var taula = document.getElementById('taulafiltro').value;
    var col = document.getElementById('colfiltro').value;
    var valuecol= document.getElementById('valuefiltro').value.split("\,");
    console.log(taula);
    console.log(col);
    console.log(valuecol);
   
    var basicFilter = {
        $schema: "http://powerbi.com/product/schema#basic",
        target: {
          table: taula,
          column: col
        },
        operator: "In",
        values: valuecol,
        filterType: models.FilterType.BasicFilter,
        requireSingleSelection: true
      }
    var reportLoadConfig = {
            type: "report",
            tokenType: models.TokenType.Embed,
            permissions: models.Permissions.Read,
            filters: [basicFilter], // dentro de la lista colocamos las variables que se definen con los filtros
            // pageName:'ReportSectionca4fb9901c0a5a020896',   esto se utiliza para definir la paguina del reporte que se desea ver
           
         
    
            // Enable this setting to remove gray shoulders from embedded report
            settings: {
                // background: models.BackgroundType.Transparent,
                panes: {
                    bookmarks: {
                        expanded: false,
                        visible: false
                    },

                    filters: {
                        expanded: false,
                        visible: false
                    },
                    
                    pageNavigation: {
                        visible: true,
                        position: models.PageNavigationPosition.Left
                    },
                
                    
        }}};

            
    
    
    $.ajax({
        type: "POST",
        url: "/getembedinfo",
        data:{work:document.getElementById('work').value,
              report:document.getElementById('report').value,},
        dataType: "json",

        success: function (data) {
            embedData = $.parseJSON(JSON.stringify(data));

            reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            // Embed Power BI report when Access token and Embed URL are available
            var report = powerbi.embed(reportContainer, reportLoadConfig);


           

            // Triggers when a report schema is successfully loaded
            report.on("loaded", function () {
                console.log("Report load successful")
            });

            

            // Triggers when a report is successfully embedded in UI
            report.on("rendered", function () {
                console.log("Report render successful")
            });



            

            // Clear any other error handler event
            report.off("error");

            // Below patch of code is for handling errors that occur during embedding
            report.on("error", function (event) {
                var errorMsg = event.detail;

                // Use errorMsg variable to log error in any destination of choice
                console.error(errorMsg);
                return;
            });
        },

        
        error: function (err) {

            // Show error container
            var errorContainer = $(".error-container");
            $(".embed-container").hide();
            errorContainer.show();

            // Format error message
            var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
            errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html(errMessageHtml);
        }
    });
    var i=document.getElementById('work').value
    const esconde= document.getElementsByClassName('esconder');
    for (let index_esconder = 0; index_esconder <= esconde.length; index_esconder++) {
        if (esconde[index_esconder].id === i){
            esconde[index_esconder].style.display ="block";
        }
        else{
            esconde[index_esconder].style.display ="none";
        }
    }

    const changeSelected = (e) => {
  const $select = document.querySelector("report");
  $select.value = i
}
});









// // Copyright (c) Microsoft Corporation.
// // Licensed under the MIT license.









// $(function () {
        
    
    
    





//     var reportContainer = $("#report-container").get(0);

//     // Initialize iframe for embedding report
//     powerbi.bootstrap(reportContainer, { type: "report" });
//     var edit = document.getElementById('edit').value
//     var pag = document.getElementById('ubicacion').value
//     var filter = document.getElementById('filter').value
//     var models = window["powerbi-client"].models;
    
//     if (edit === '1'|| edit === 'Off'){
//         if (pag=='1' && filter=='1') {var reportLoadConfig = {
//             type: "report",
//             tokenType: models.TokenType.Embed,
//             permissions: models.Permissions.Create,
         
    
//             // Enable this setting to remove gray shoulders from embedded report
//             settings: {
//                 // background: models.BackgroundType.Transparent,
//                 panes: {
//                     bookmarks: {
//                         expanded: false,
//                         visible: true
//                     },
                   
//                     filters: {
//                         expanded: false,
//                         visible: true
//                     },
//                     pageNavigation: {
//                         visible: true,
//                         position: models.PageNavigationPosition.Left
//                     },
                
                    
//         }}};}

//           else if (pag=='1' && filter=='2'){var reportLoadConfig = {
//             type: "report",
//             tokenType: models.TokenType.Embed,
//             permissions: models.Permissions.Create,
         
    
//             // Enable this setting to remove gray shoulders from embedded report
//             settings: {
//                 // background: models.BackgroundType.Transparent,
//                 panes: {
//                     bookmarks: {
//                         expanded: false,
//                         visible: true
//                     },
                   
//                     filters: {
//                         expanded: false,
//                         visible: false
//                     },
//                     pageNavigation: {
//                         visible: true,
//                         position: models.PageNavigationPosition.Left
//                     },
                
                    
//         }}};}

//         else if (pag=='2' && filter=='2'){var reportLoadConfig = {
//             type: "report",
//             tokenType: models.TokenType.Embed,
//             permissions: models.Permissions.Create,
         
    
//             // Enable this setting to remove gray shoulders from embedded report
//             settings: {
//                 // background: models.BackgroundType.Transparent,
//                 panes: {
//                     bookmarks: {
//                         expanded: false,
//                         visible: true
//                     },
                   
//                     filters: {
//                         expanded: false,
//                         visible: false
//                     },
//                     pageNavigation: {
//                         visible: true,
//                         position: models.PageNavigationPosition.Down
//                     },
                
                    
//         }}};}


//         else {var reportLoadConfig = {
//             type: "report",
//             tokenType: models.TokenType.Embed,
//             permissions: models.Permissions.Create,
         
    
//             // Enable this setting to remove gray shoulders from embedded report
//             settings: {
//                 // background: models.BackgroundType.Transparent,
//                 panes: {
//                     bookmarks: {
//                         expanded: false,
//                         visible: true
//                     },
                   
//                     filters: {
//                         expanded: false,
//                         visible: true
//                     },
//                     pageNavigation: {
//                         visible: true,
//                         position: models.PageNavigationPosition.Down
//                     },
                
                    
//         }}};}}








//         else {var reportLoadConfig = {
//             type: "report",
//             tokenType: models.TokenType.Embed,
//             permissions: models.Permissions.Create,
//             viewMode: models.ViewMode.Edit,
    
//             // Enable this setting to remove gray shoulders from embedded report
//             settings: {
//                 // background: models.BackgroundType.Transparent,
//                 panes: {
//                     bookmarks: {
//                         expanded: false,
//                         visible: false
//                     },
//                     fields: {
//                         expanded: false,
//                         expanded: true
//                     },
//                     filters: {
//                         expanded: false,
//                         visible: true
//                     },
//                     pageNavigation: {
//                         visible: true,
//                         position: models.PageNavigationPosition.Left
//                     },
//                     selection: {
//                         expanded: false,
//                         visible: false
//                     },
//                     syncSlicers: {
//                         expanded: false,
//                         visible: false
//                     },
//                     visualizations: {
//                         expanded: false,
//                         visible: true
//                     }
//         }}};
//             }

            
    
    
//     $.ajax({
//         type: "POST",
//         url: "/getembedinfo",
//         data:{work:document.getElementById('work').value,
//               report:document.getElementById('report').value,},
//         dataType: "json",
//         success: function (data) {
//             embedData = $.parseJSON(JSON.stringify(data));

//             reportLoadConfig.accessToken = embedData.accessToken;

//             // You can embed different reports as per your need
//             reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

//             // Use the token expiry to regenerate Embed token for seamless end user experience
//             // Refer https://aka.ms/RefreshEmbedToken
//             tokenExpiry = embedData.tokenExpiry;

//             // Embed Power BI report when Access token and Embed URL are available
//             var report = powerbi.embed(reportContainer, reportLoadConfig);

            

//             // Triggers when a report schema is successfully loaded
//             report.on("loaded", function () {
//                 console.log("Report load successful")
//             });

            

//             // Triggers when a report is successfully embedded in UI
//             report.on("rendered", function () {
//                 console.log("Report render successful")
//             });



            

//             // Clear any other error handler event
//             report.off("error");

//             // Below patch of code is for handling errors that occur during embedding
//             report.on("error", function (event) {
//                 var errorMsg = event.detail;

//                 // Use errorMsg variable to log error in any destination of choice
//                 console.error(errorMsg);
//                 return;
//             });
//         },

        
//         error: function (err) {

//             // Show error container
//             var errorContainer = $(".error-container");
//             $(".embed-container").hide();
//             errorContainer.show();

//             // Format error message
//             var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
//             errMessageHtml = errMessageHtml.split("\n").join("<br/>")

//             // Show error message on UI
//             errorContainer.html(errMessageHtml);
//         }
//     });
//     var i=document.getElementById('work').value
//     const esconde= document.getElementsByClassName('esconder');
//     for (let index_esconder = 0; index_esconder <= esconde.length; index_esconder++) {
//         if (esconde[index_esconder].id === i){
//             esconde[index_esconder].style.display ="block";
//         }
//         else{
//             esconde[index_esconder].style.display ="none";
//         }
//     }

//     const changeSelected = (e) => {
//   const $select = document.querySelector("report");
//   $select.value = i
// }
// });