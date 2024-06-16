import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from "@angular/material/dialog";
import { Store } from '@ngrx/store';
import { FileUploader } from 'ng2-file-upload';

import * as actions from '../../state/actions';

import {
  AbstractControl,
  UntypedFormArray,
  UntypedFormControl,
  UntypedFormGroup,
  Validators
} from '@angular/forms';

import { AddVideoModel } from '../../models'

@Component({
  selector: 'app-add-video',
  templateUrl: './add-video.component.html',
  styleUrl: './add-video.component.sass'
})
export class AddVideoComponent implements OnInit{
  form: UntypedFormGroup;
  uploader: FileUploader = new FileUploader({ url: 'http://example.com/upload' });

  constructor( 
    private dialogRef: MatDialogRef<AddVideoComponent>,
    private store$: Store ){
    this.form = new UntypedFormGroup(
      {
        link: new UntypedFormControl,
        description: new UntypedFormControl
      },
    );
  }
  ngOnInit(): void {

  }
  onFileChange(event: any) {
    const file = event.target.files[0];
    this.uploader.addToQueue([file]);
  }

  uploadFile() {
    this.uploader.uploadAll();
  }

  add(){
    if (this.form.valid) {
      const data = this.form.getRawValue() as AddVideoModel;
      this.store$.dispatch(actions.addVideo({addVideoModel: data}));
      this.dialogRef.close();
    }
    else{
      this.form.markAllAsTouched();
    }
  }
}
