import { Validators, AbstractControl, ValidatorFn } from '@angular/forms';

export class AppValidador extends Validators {

  private static parentControlsValue(control: AbstractControl, controlKey : string) {
    if (control != undefined &&  control.parent != undefined && control.parent.controls != undefined ){
      const parentControls = control.parent.controls
      if (parentControls[controlKey] == undefined) {
        console.error("The key " + controlKey + " don't exists in this validator control.");
        return null
      }

      return parentControls[controlKey].value
    }

  }
  
  static match(controlKey : string): ValidatorFn {
    return (control: AbstractControl): { [key: string]: boolean } | null => {

      const valueToMatch = AppValidador.parentControlsValue(control, controlKey)
      if (control.value !== undefined && control.value != valueToMatch) {
        return { 'match': true };
      }
      return null;
    };
  }
}