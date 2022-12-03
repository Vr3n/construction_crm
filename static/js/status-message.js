// eslint no-undef: 0
// eslint no-unused-vars: 0

const statusMessageComponent = () => {
    return {
        // data
        show: false,
        colors: {},
        eventName: undefined,
        eventParams: {},
        statusMessageText: '',
        statusMessageTimeout: undefined,

        infoBackground: 'alert-info',
        successBackground: 'alert-success',
        warningBackground: 'alert-warning',
        dangerBackground: 'alert-danger',
    },
    handleStatusMessageClick = () => {
        if (this.eventName) {
            this.$nextTick(() => {
                hDispatch(this.eventName, this.eventParams);
            })
        }
        this.statusMessageClear();
    },
    processContext = (context) => {
        let result = {};
        if (typeof(context) === 'string') {
            result.message = context;
        } else if (typeof(context) === 'object') {
            if (context.message === "undefined") {
                console.error("Context must contain non-empty 'message'.");
                return false;
            }
            result.message = context.message;
            result.messageType = context.messageType;
            result.timeout = context.timeout;

            if (context.eventName) {
                this.eventName = context.eventName;
                this.eventParams = context.eventParams;
            } else {
                this.eventName = undefined;
                this.eventParams = {};
            }
        } else {
            console.error("Context must be object or string");
            return false;
        }

        // timeout
        if (!context.timeout) {
            result.timeout = defaultMessageTimeout;
        }
        return result;
    },
    statusMessageClear = () => {
        clearTimeout(this.statusMessageTimeout);
        this.show = false;
        setTimeout(() => {
            // clear the text.
            this.statusMessageText = '';

            // clear any events.
            this.eventName = "";
            this.eventParams = {};
        }, defaultTransitionDuration)
    }
}