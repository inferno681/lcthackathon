import { HttpErrorResponse } from "@angular/common/http";
import { createAction, props } from '@ngrx/store';

import { ContentModel } from '../../models'

export const empty = createAction('[Compute] empty');

export const loadContent = createAction('[Search] load content', props<{ query: string }>());
export const loadContentSuccess = createAction('[Search] load content success', props<{ content: ContentModel[] }>());
export const loadContentFails = createAction('[Search] load content fails', props<{ error: HttpErrorResponse }>());