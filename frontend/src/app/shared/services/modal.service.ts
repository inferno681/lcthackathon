import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';

@Injectable({
    providedIn: 'root'
})
export class ModalService {

    constructor(private modals: MatDialog) { }

    show<T>(content: any, config: MatDialogConfig): Observable<T> {
        const dialog = this.modals.open(content, config);
        return dialog.afterClosed();
    }

    closeAll(): void {
        this.modals.closeAll();
    }
}