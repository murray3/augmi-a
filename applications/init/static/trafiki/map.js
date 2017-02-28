MapView = (function(){
	var _self;
	return _self = Ext.extend(Ext.Map, {
		initComponent: function(){
			
			var me = this;
			this.listeners = {
				scope: this,
				maprender: function(comp, map){
					//console.log(this, me, marker, map);
					var marker = new google.maps.Marker({
						position: new google.maps.LatLng(this.o && this.o.pos && this.o.pos.lat || 59, this.o && this.o.pos && this.o.pos.lon || 12),
						title: this.o.title,
						map: map
					});
					
				}
			}
			
			//console.log(this, this.pos);
			/*navigator.geolocation.getCurrentPosition(
                function(position) { map.setCenter(new google.maps.LatLng(position.coords.latitude, position.coords.longitude)); }, 
                function(msg){ console.error(msg); }
            );*/
				
			this.mapOptions = {
                center : new google.maps.LatLng(this.o && this.o.pos && this.o.pos.lat || 59, this.o && this.o.pos && this.o.pos.lon || 12),
                zoom : 15,
                mapTypeId : google.maps.MapTypeId.ROADMAP,
                navigationControl: true,
                navigationControlOptions: {
                    style: google.maps.NavigationControlStyle.DEFAULT
                }
            }
		},
		
		
	});
})();