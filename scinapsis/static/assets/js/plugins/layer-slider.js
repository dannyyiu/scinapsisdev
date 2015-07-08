var LayerSlider = function () {

    return {

        //Layer Slider
        initLayerSlider: function () {
		    $(document).ready(function(){
		        jQuery("#layerslider").layerSlider({
			        responsive : true,
			        responsiveUnder : 960,
			        layersContainer : 960,
			        skinsPath: '/static/assets/plugins/layer-slider/layerslider/skins/',
                    skin: 'glass'
			    });
		    });
        }

    };
}();