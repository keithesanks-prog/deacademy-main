import csv
import json
from datetime import datetime
import os

class CSVtoJSONConverter:
    """Convert CSV sales data to JSON format for API integration."""
    
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []
        
    def read_csv(self):
        """Read CSV file and store data."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                self.data = list(csv_reader)
            print(f"✓ Successfully read {len(self.data)} records from {self.csv_file}")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{self.csv_file}' not found")
            return False
        except Exception as e:
            print(f"✗ Error reading CSV: {str(e)}")
            return False
    
    def convert_data_types(self):
        """Convert string values to appropriate data types."""
        for record in self.data:
            # Convert numeric fields
            if 'Quantity' in record:
                record['Quantity'] = int(record['Quantity'])
            if 'Unit_Price' in record:
                record['Unit_Price'] = float(record['Unit_Price'])
            if 'Total' in record:
                record['Total'] = float(record['Total'])
        
        print(f"✓ Converted data types for {len(self.data)} records")
    
    def save_as_json(self, output_file='sales_data.json', indent=2):
        """Save data as JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=indent)
            
            file_size = os.path.getsize(output_file)
            print(f"✓ Saved JSON to {output_file} ({file_size} bytes)")
            return output_file
        except Exception as e:
            print(f"✗ Error saving JSON: {str(e)}")
            return None
    
    def create_api_payload(self, batch_size=None):
        """Create API-ready JSON payload with metadata."""
        payload = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "source": self.csv_file,
                "total_records": len(self.data),
                "version": "1.0"
            },
            "data": self.data if not batch_size else self.data[:batch_size]
        }
        return payload
    
    def save_api_payload(self, output_file='api_payload.json', batch_size=None):
        """Save API-ready payload with metadata."""
        try:
            payload = self.create_api_payload(batch_size)
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(payload, file, indent=2)
            
            print(f"✓ Created API payload: {output_file}")
            print(f"  - Total records: {payload['metadata']['total_records']}")
            print(f"  - Timestamp: {payload['metadata']['timestamp']}")
            return output_file
        except Exception as e:
            print(f"✗ Error creating API payload: {str(e)}")
            return None
    
    def get_summary_stats(self):
        """Calculate summary statistics from the data."""
        if not self.data:
            return None
        
        total_revenue = sum(float(record.get('Total', 0)) for record in self.data)
        total_quantity = sum(int(record.get('Quantity', 0)) for record in self.data)
        
        # Group by product
        products = {}
        for record in self.data:
            product = record.get('Product', 'Unknown')
            if product not in products:
                products[product] = {'count': 0, 'revenue': 0}
            products[product]['count'] += 1
            products[product]['revenue'] += float(record.get('Total', 0))
        
        # Group by region
        regions = {}
        for record in self.data:
            region = record.get('Region', 'Unknown')
            if region not in regions:
                regions[region] = {'count': 0, 'revenue': 0}
            regions[region]['count'] += 1
            regions[region]['revenue'] += float(record.get('Total', 0))
        
        summary = {
            "total_transactions": len(self.data),
            "total_revenue": round(total_revenue, 2),
            "total_quantity": total_quantity,
            "average_transaction": round(total_revenue / len(self.data), 2),
            "products": products,
            "regions": regions
        }
        
        return summary
    
    def save_with_summary(self, output_file='sales_with_summary.json'):
        """Save data with summary statistics."""
        try:
            summary = self.get_summary_stats()
            
            output = {
                "summary": summary,
                "transactions": self.data
            }
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(output, file, indent=2)
            
            print(f"✓ Saved data with summary: {output_file}")
            print(f"  - Total Revenue: ${summary['total_revenue']:,.2f}")
            print(f"  - Total Transactions: {summary['total_transactions']}")
            return output_file
        except Exception as e:
            print(f"✗ Error saving with summary: {str(e)}")
            return None
    
    def display_preview(self, num_records=3):
        """Display preview of the data."""
        print(f"\n{'='*60}")
        print(f"DATA PREVIEW (First {num_records} records)")
        print(f"{'='*60}")
        
        for i, record in enumerate(self.data[:num_records], 1):
            print(f"\nRecord {i}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
        
        print(f"\n{'='*60}\n")


def main():
    """Main function to demonstrate CSV to JSON conversion."""
    
    print("="*60)
    print("CSV TO JSON CONVERTER FOR SALES DATA")
    print("="*60)
    print()
    
    # Initialize converter
    csv_file = 'sales_data.csv'
    converter = CSVtoJSONConverter(csv_file)
    
    # Read CSV
    if not converter.read_csv():
        return
    
    # Convert data types
    converter.convert_data_types()
    
    # Display preview
    converter.display_preview(3)
    
    # Option 1: Simple JSON conversion
    print("\n[1] Creating simple JSON file...")
    converter.save_as_json('sales_data.json')
    
    # Option 2: API-ready payload with metadata
    print("\n[2] Creating API-ready payload...")
    converter.save_api_payload('api_payload.json')
    
    # Option 3: JSON with summary statistics
    print("\n[3] Creating JSON with summary statistics...")
    converter.save_with_summary('sales_with_summary.json')
    
    # Option 4: Batch payload (first 5 records for testing)
    print("\n[4] Creating batch payload (5 records)...")
    converter.save_api_payload('api_payload_batch.json', batch_size=5)
    
    print("\n" + "="*60)
    print("CONVERSION COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. sales_data.json - Simple array of transactions")
    print("  2. api_payload.json - API-ready with metadata")
    print("  3. sales_with_summary.json - Includes summary stats")
    print("  4. api_payload_batch.json - Batch of 5 records")
    print("\nAll files are ready to be sent via API!")
    print("="*60)


if __name__ == "__main__":
    main()
