Function.prototype.bind = function(scope, args, append){
	return scope ? Ext.createDelegate(this, scope, args, append) : this;
};

