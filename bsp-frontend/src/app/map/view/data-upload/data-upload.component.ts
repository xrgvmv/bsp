import { Component, Input, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {MapService} from '../../service/map.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-data-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './data-upload.component.html',
  styleUrls: ['./data-upload.component.css'], 
})

export class DataUploadComponent implements OnInit {
  @Input() map: L.Map | undefined;
  @Input() mapService: MapService | undefined;

  message: string = '';

  constructor(private api: MapService) {}

  ngOnInit(): void {

  }

  submitDynamicForm(formType: string, jsonInput: string): void {
    let formData;

    try {
      formData = JSON.parse(jsonInput);
    } catch (e) {
      this.message = 'Nieprawidłowy JSON';
      return;
    }

    switch (formType) { 
      case 'droneid_info':
        this.api.postDroneidInfo(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      case 'remoteid_info':
        this.api.postRemoteidInfo(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      case 'droneid_flight':
        this.api.postDroneidFlight(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      case 'remoteid_flight':
        this.api.postRemoteidFlight(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      case 'droneid_movement':
        this.api.postDroneidMovement(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      case 'remoteid_movement':
        this.api.postRemoteidMovement(formData).subscribe({
        next: (response: any) => {
          console.log('Sukces:', response);
        },
        error: (err: any) => {
          console.error('Błąd podczas wysyłania danych:', err);
        }
        });
        break;
      default:
        this.message = 'Nieznany typ formularza';
        return;
    }
  }

  showForm(num: number): void {
    const forms = document.querySelectorAll('.form-box');
    forms.forEach(form => form.classList.remove('active'));

    const selectedForm = document.getElementById('form' + num);
    if (selectedForm) {
      selectedForm.classList.add('active');
    }
  }

  submitForm(formType: string): void {
    const jsonInput = (document.getElementById('json_' + formType) as HTMLInputElement)?.value;
    
    if (!jsonInput) {
      return;
    }

    this.submitDynamicForm(formType, jsonInput);
  }
}