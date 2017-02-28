TimePicker = (function(){
    var _self;
    return _self = Ext.extend(Ext.Picker, {        
        initComponent: function(){
			var hourData = [];
			for(var i = 0; i < 24; i++){ hourData.push({ text: (i < 10 ? "0" : "")+i, value: i }); }
            var minuteData = [];
			for(var i = 0; i < 60; i++){ minuteData.push({ text: (i < 10 ? "0" : "")+i, value: i }); }
			
			this.date = this.date || new Date();
			
			this.slots = [{
	            name : 'hour',
	            title: 'Hour',
	            data : hourData,
				align: 'right'
	        },
			{
	            name : 'minute',
	            title: 'Minute',
	            data : minuteData,
				align: 'left'
	        }
			];

			if (this.value) {
	            var value = this.value;
	            if (Ext.isDate(value)) {
	                this.value = {
	                    hour : value.getHours(),
	                    minute: value.getMinutes()
	                };
	            } else if (Ext.isObject(value)) {
	                this.value = value;
	            };
	        }
            
            Ext.DatePicker.superclass.initComponent.call(this);
        },
		
		getValue: function() {
	        var value = Ext.DatePicker.superclass.getValue.call(this);
	        return new Date(0, 0, 0, value.hour, value.minute);
	    }
    });
})();
