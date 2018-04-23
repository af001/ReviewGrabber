# ReviewGrabber
Extract product reviews from Amazon and store the results in a SQL database for future analysis. This script is for educational purposes only and may violate Amazon's Terms of Service depending on usage. Please read the full [Terms of Service](https://www.amazon.com/gp/help/customer/display.html/ref=footer_cou?ie=UTF8&nodeId=508088) provided by Amazon via the provided link.

### Installation

``` python
git clone https://github.com/af001/ReviewGrabber.git
cd ReviewGrabber
pip install -r requirements.txt
```
### Usage

```bash
python reviewgrabber.py
```

```python
help
help <get save exit batch>
get <url>                           # Get all reviews.
batch manual <url>                  # Get all reviews from text file of URLs. Manually save.
batch auto <url>                    # Get all reviews from text file of URLs. Auto save to default table.
save <table_name>                   # Save all reviews, not batch auto, into a table named <table_name>
inspect tables			    # View available tables in SQLalchemy database.
csv <table_name>		    # Export table into CSV file for viewing in the React App
exit                                # Exit the console application. No save on exit.
```
### Example

Terminal
![alt text](https://github.com/af001/ReviewGrabber/blob/master/screenshots/terminal.png "Terminal View")
Sqlite3
![alt text](https://github.com/af001/ReviewGrabber/blob/master/screenshots/sqlite.png "Sqlite View")

### Schema
```sqlite
sqlite> .schema wireless
CREATE TABLE wireless (
	author TEXT,
	author_profile TEXT,
	helpful BIGINT,
	image_available BIGINT,
	link TEXT,
	product_id TEXT,
	rating BIGINT,
	review TEXT,
	review_date TEXT,
	review_id TEXT,
	title TEXT
);
```
### React App Viewer
```bash
cd amazongrabber
yarn install                           # Only run on first download
yarn start                             # Start the react app
```
Output reviews from sqlalchemy to CSV
![alt text](https://github.com/af001/ReviewGrabber/blob/master/screenshots/AG2.png "Terminal View")
React App Viewer
![alt text](https://github.com/af001/ReviewGrabber/blob/master/screenshots/ReactApp.png "ReactApp")
Filter Reviews
![alt text](https://github.com/af001/ReviewGrabber/blob/master/screenshots/ReactApp4.png "ReactApp")

### Liability Disclaimer

THIS SOFTWARE IS PROVIDED 'AS IS' AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANT ABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
