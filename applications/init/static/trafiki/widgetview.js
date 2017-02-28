WidgetView = (function(){
	var _self;
	return _self = Ext.extend(DashboardView, {
		initComponent: function(){
			this.listeners = {
				deactivate: this.onDeactivate
			};
			
			_self.superclass.initComponent.call(this);
		},
		
		initEvents: function(){
			var me = this;
			_self.superclass.initEvents.call(this);
			me.mon(me.el, {
	            scope: me,
	            
	            touchstart : me.onTouchStart,
	            touchmove  : me.onTouchMove,
	            touchend   : me.onTouchEnd
	        });
			
		},
		
		flex: 1,
		touching: false,
		drawn: false,
		goodStroke: '#0f0',
		badStroke: '#f00',
		
		from: null,
		via: [],
		to: null,
		
		clearRoute: function(){
			if(this.from){ this.from.el.removeClass('from'); this.from = null; }
			this.via.forEach(function(widget){ widget.el.removeClass('via'); });
			this.via = [];
			if(this.to){ this.to.el.removeClass('to'); this.to = null; }
			this.d = 0;
			
			this.ctx.save();
			this.ctx.clearRect(0, 0, this.canvas.getWidth(), this.canvas.getHeight());
		},
		
		onTouchStart: function(e){
			this.clearRoute();
			this.offsets = this.el.getOffsetsTo(document.body);
		},
		
		onTouchMove: function(e){
			var x = e.pageX - this.offsets[0], y = e.pageY - this.offsets[1];
			if (!this.touching && this.sortable.disabled) {
				var tmp, from = this.getWidgetFromPoint(e);
				if (from) {
					this.touches = [];
					this.from = from;
					from.el.addClass('from');
				}
				
				this.ctx.strokeStyle = from ? this.goodStroke : this.badStroke;
				this.ctx.moveTo(x, y);
				this.ctx.beginPath();
				this.touching = true;
			}
			
			if(this.touching && this.sortable.disabled){
				this.d += Math.abs(e.previousDeltaX) + Math.abs(e.previousDeltaY);
				/*if(this.touches.length == 7){
					this.touches.shift();
				}
				this.touches.push([e.pageX, e.pageY]);
				if(this.touches.length == 7){
					//console.log('hej', this.touches.join(", "));
					var ts = this.touches,
						v1 = $V([ts[0][0] - ts[3][0], ts[0][1] - ts[3][1]]),
						v2 = $V([ts[6][0] - ts[3][0], ts[6][1] - ts[3][1]]),
						angle = (Math.PI - v1.angleFrom(v2)) * 180/Math.PI;
						
					if(angle > 70){
						console.log(angle, v1.modulus(), v2.modulus());
						this.ctx.closePath();
						this.ctx.beginPath();
						this.ctx.arc(ts[3][0], ts[3][1], 5, 0, Math.PI*2, true); 
						this.ctx.closePath();
						this.ctx.fill();
						this.ctx.beginPath();
					}
				}*/
				
				if(e.previousDeltaTime > 300){
					var widget = this.getWidgetFromPoint(e);
					if (widget) {
						widget.el.addClass('via');
						this.via.push(widget);
					}
				}						
				
				this.drawn = true;
                this.ctx.lineTo(x, y);
                this.ctx.stroke();
                this.ctx.moveTo(x, y);
			}
		},
		
		onTouchEnd: function(e){
			this.touching = false;
			if(this.from && this.d > 10){
				var widget = this.getWidgetFromPoint(e);
				if (widget) {
					widget.el.addClass('to');
					this.to = widget;
				} else { this.clearRoute(); return; }
				
				app.getRoute([this.from].concat(this.via).concat(this.to));
				/*async.series(
					[this.from]
					.concat(this.via)
					.concat(this.to)
					.map(function(item, i, arr){ 
						return Ext.createDelegate(item.getPoint, item, [i == 0 ? 'from' : (i == arr.length - 1 ? 'to' : 'via')], true ); 
					}), 
					
					function(err, res){
						console.log('res', res);
					}
				);*/
			}
			if (this.drawn) {
				this.drawn = false;
				this.ctx.save();
				this.ctx.clearRect(0, 0, this.canvas.getWidth(), this.canvas.getHeight());
			}
		},
		
		afterLayout: function(){
			if(!this.canvas){
				this.canvas = this.el.createChild({
	                tag: 'canvas',
	                html: '',
	                cls: 'canvasOverlay',
					width: this.el.getWidth(),
					height: this.el.getHeight(),
					//style: 'height: ' + el.getHeight() + 'px'
	            });
				this.ctx = this.canvas.dom.getContext("2d");
				this.ctx.strokeStyle = "#0f0";
			} else {
				this.canvas.dom.height = this.el.getHeight();
				this.ctx.lineWidth = 3;
				this.ctx.lineCap = 'round';
			}
		},
		
		onDeactivate: function(){
			this.clearRoute();
		}
	});
})();