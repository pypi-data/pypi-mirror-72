element = layui.element;
layer = layui.layer;
laydata = layui.layer;
laypage = layui.laypage;
table = layui.table;
form = layui.form;
upload = layui.upload;
transfer = layui.transfer;
tree = layui.tree;
colorpicker = layui.colorpicker;
slider = layui.slider;
rate = layui.rate;
carousel = layui.carousel;
flow = layui.flow;
utill = layui.utill;
code = layui.code;

function __$RANDOM(lowerValue, upperValue) {
    return Math.floor(Math.random() * (upperValue - lowerValue + 1) + lowerValue);
}

function MassageBox(str) {
    return layer.msg(str);
}

function AlertBox(str) {
    return layer.alert(str);
}

function LoadsBox(style = null, Second = 1) {
    if (style == null) {
        style = __$RANDOM(0, 2);
        console.log(style);
    }
    return layer.load(style, { time: Second * 1000 });
}

function CloseBox(ObjBox) {
    layer.close(ObjBox);
}

function CloseAllBox(BoxType = null) {
    if (BoxType == null) {
        layer.closeAll();
        return null;
    }
    if (BoxType != null) {
        layer.closeAll(BoxType);
        return null;
    }
}

function IframeBox(url, scrollBar = true) {
    if (scrollBar == true) {
        layer.open({
            type: 2,
            content: url
        })
    } else if (scrollBar == false) {
        layer.open({
            type: 2,
            content: ['http://sentsin.com', "no"]
        })
    }