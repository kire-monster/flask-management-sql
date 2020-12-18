function sqlExec(){
    $.ajax({
        url: '/sql',
        method: 'POST',
        data: {
            'query': $("#consulta").val(),
            'db': $("#dbname").val()
        }
    }).done(function(resp){
        

        
        var template = Handlebars.compile(`
        
        <h3>{{mensaje}}</h3>
        <table class="tb-result">
            <thead class="thead-dark">
                <tr>
                    {{#each columns}}
                    <th>{{this}}</th>
                    {{/each}}
                </tr>
            </thead>
            <tbody>
            
                {{#each respuesta}}
                    <tr>
                        {{#each this}}
                            <td>{{this}}</td>
                        {{/each}}
                    </tr>
                {{/each}}

            </tbody>
        </table>
        
        `)
        
        $("#div-respuesta").html(template({ 'respuesta': resp.Resultado, 'mensaje': resp.Mensaje, 'columns': resp.Columns }))
        $("#label-query").html('<b>sql:</b> <code>' + resp.Query +'</code>')
    }).fail(function(){
        console.log("Error")
    })
}



$("#btn-Consultar").click(function(){
    sqlExec()
})

$("#consulta").bind('keydown', 'ctrl+a', function(){
    sqlExec()
});