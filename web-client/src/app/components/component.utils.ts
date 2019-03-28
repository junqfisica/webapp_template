import { NotificationService } from '../services/notification/notification.service';

export abstract class ComponentUtils {

    // bsConfig = Object.assign({}, {locale: 'de', containerClass: 'theme-dark-blue', dateInputFormat: 'DD.MM.YYYY'});
  
    constructor(private __notificationService: NotificationService) {
  
    }
  
    public showSuccessMessage(message: string) {
      this.__notificationService.showSuccessMessage(message);
    }

    public showWarningMessage(message: string) {
        this.__notificationService.showWarningMessage(message);
    }
  
    public showErrorMessage(message: string) {
      this.__notificationService.showErrorMessage(message);
    }
  }