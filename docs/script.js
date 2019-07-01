window.onload = () => {
    let container = document.getElementById("content_container");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
            container.innerHTML = page_content(JSON.parse(xhttp.responseText));
    };
    xhttp.open("GET", "package.json", true);
    xhttp.send();
};

function page_content(jsonObj) {
    let result = "<h1>" + jsonObj.title + "</h1>";
    result += "<hr><p>" + jsonObj.description + "</p><br>";
    for (let section of jsonObj.sections)
        result += section_content(section);
    return result;
}

function section_content(jsonObj) {
    let result = "<div id=\"" + jsonObj.title + "\">";
    result += "<h2>" + jsonObj.title + "</h2><hr>";
    if (jsonObj.properties) {
        result += "<ul>";
        for (let property of jsonObj.properties)
            result += property_content(property);
        result += "</ul>";
    }
    if (jsonObj.classes) {
        result += "<ul>";
        for (let class_obj of jsonObj.classes)
            result += class_content(class_obj);
        result += "</ul>";
    }
    result += "</div>";
    return result;
}

function property_content(jsonObj) {
    let result = "<div class=\"code_line\"><p><b>" + jsonObj.name + "</b></p></div>";
    result += "<p>( " + jsonObj.datatype + " )";
    if (jsonObj.description)
        result += " - " + jsonObj.description;
    result += "</p><br>";
    return result;
}

function class_content(jsonObj) {
    let result = "<div class=\"class " + jsonObj.name + "\">";
    result += "<div class=\"code_line\"><p><i>class</i> ";
    if (jsonObj.prefix)
        result += jsonObj.prefix + " ";
    result += "<b>" + jsonObj.name + "(</b><i>";
    if (jsonObj.parameters) {
        let param_strings = [];
        for (let param of jsonObj.parameters) {
            if (param.default) {
                param_strings.push(param.name + "=" + param.default);
            } else {
                param_strings.push(param.name);
            }
        }
        result += param_strings.join(", ");
    }
    result += "</i><b>)</b></p></div><div class=\"indent\">";
    if (jsonObj.description)
        result += "<p>" + jsonObj.description + "</p>";
    if (jsonObj.parameters) {
        result += "<p><b>Parameters</b></p><ul>";
        for (let param of jsonObj.parameters)
            result += "<li>" + parameter_content(param) + "</li>";
        result += "</ul>"
    }
    if (jsonObj.raises) {
        result += "<p><b>Raises</b></p><ul>";
        for (let exception of jsonObj.raises)
            result += "<li>" + exception_content(exception) + "</li>";
        result += "</ul><br>";
    }
    if (jsonObj.properties)
        for (let property of jsonObj.properties)
            result += property_content(property);
    if (jsonObj.methods)
        for (let method of jsonObj.methods)
            result += method_content(method);
    result += "</div></div>";
    return result;
}

function parameter_content(jsonObj) {
    let result = "<p><b>" + jsonObj.name + "</b> "
    if (jsonObj.datatype)
        result += "( " + jsonObj.datatype + " )";
    if (jsonObj.description)
        result += " - " + jsonObj.description;
    result += "</p>";
    return result;
}

function method_content(jsonObj) {
    let result = "<div class=\"code_line\"><p>";
    if (jsonObj.async)
        result += "<i>await</i> ";
    result += "<b>" + jsonObj.name + "(</b><i>";
    if (jsonObj.parameters) {
        let params = [];
        for (let param of jsonObj.parameters) {
            if (param.default) {
                params.push(param.name + "=" + param.default);
            } else {
                params.push(param.name);
            }
        }
        result += params.join(", ");
    }
    result += "</i><b>)</b></p></div>";
    result += "<div class=\"indent\"><p>" + jsonObj.description + "</p>";
    if (jsonObj.parameters) {
        result += "<p><b>Parameters</b></p><ul>";
        for (let param of jsonObj.parameters)
            result += "<li>" + parameter_content(param) + "</li>";
        result += "</ul>"
    }
    if (jsonObj.raises) {
        result += "<p><b>Raises</b></p><ul>";
        for (let exception of jsonObj.raises)
            result += "<li>" + exception_content(exception) + "</li>";
        result += "</ul><br>";
    }
    if (jsonObj.returns) {
        result += "<p><b>Returns</b></p><ul>";
        for (let return_value of jsonObj.returns)
            result += "<li>" + return_content(return_value) + "</li>";
        result += "</ul><br>";
    }
    result += "</div>";
    return result;
}

function exception_content(jsonObj) {
    return "<p>" + jsonObj.exception + " - " + jsonObj.condition + "</p>";
}

function return_content(jsonObj) {
    return "<p>" + jsonObj.datatype + " - " + jsonObj.description + "</p>";
}