import { HttpErrorResponse } from "@angular/common/http";
import { createAction, props } from "@ngrx/store";

import { AddVideoModel } from '../models'

export const showAddVideoPopups = createAction('[Layout] show add video popups');
export const addVideo = createAction('[Layout] add video', props<{ addVideoModel: AddVideoModel }>());
